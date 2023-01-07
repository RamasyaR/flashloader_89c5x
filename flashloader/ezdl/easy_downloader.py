import logging
from typing import Optional, Union

import serial

from flashloader.constants import Ecode, MCUMemorySize, ProgVoltages, SupportedMCU
from flashloader.hex_processing import load_hex, save_hex

from .decorators import check_chip, disconnect_if_error, is_connected
from .enums import Commands
from .messages import InfoMessage, PGMMessage
from .utils import convert_counter, convert_str_to_enum, send_data

logger = logging.getLogger('ezdl_flasher')


class EZDLFlasher:
    def __init__(self):
        self._dev: Optional[serial.Serial] = None

    def _is_connected(self) -> bool:
        try:
            if not isinstance(self._dev, serial.Serial):
                return False
            elif not self._dev.is_open:
                return False
            elif not isinstance(self._get_programmer_title(), str):
                return False
            else:
                return True
        except Exception as ex:
            logger.error(f'Error get connection state: {ex}.')
            return False

    @property
    def device(self) -> Optional[str]:
        return self._dev.name if self._is_connected() else None

    def connect(self, device: str) -> Union[str, Ecode]:
        if self._is_connected():
            logger.info('Programmer is already connected.')
            return Ecode.OK

        try:
            self._dev = serial.Serial(device, 9600, timeout=5)
        except Exception as ex:
            logger.error(f'Open programmer on {device} failed: {ex}.')
            return Ecode.CONNECTION_ERROR

        return self.get_title()

    def disconnect(self) -> Ecode:
        if not self._is_connected():
            logger.info('Programmer is already disconnected.')
            return Ecode.OK

        try:
            self._dev.close()
        except Exception as ex:
            logger.error(f'Disconnect programmer failed, clearing device variable, error: {ex}.')
            return Ecode.DISCONNECTION_ERROR
        else:
            return Ecode.OK
        finally:
            self._dev = None

    @is_connected
    @disconnect_if_error
    def get_title(self) -> Union[str, Ecode]:
        return self._get_programmer_title()

    def _get_programmer_title(self) -> Union[str, Ecode]:
        try:
            response = send_data(self._dev, Commands.GET_TITLE)
        except Exception as ex:
            logger.error(f'Error getting programmer title: {ex}.')
            return Ecode.GETTING_TITLE_FAILED
        else:
            return " ".join(response.replace('>', '').split())

    @is_connected
    @disconnect_if_error
    def get_info(self) -> Union[InfoMessage, Ecode]:
        return self._get_info()

    def _get_info(self) -> Union[InfoMessage, Ecode]:
        try:
            response = send_data(self._dev, Commands.GET_INFO)
        except Exception as ex:
            logger.error(f'Error getting chip information: {ex}.')
            return Ecode.GETTING_INFO_DATA_FAILED

        try:
            response = response.split()
            mcu_properties = response[response.index('found') + 1].split('-')
            if len(mcu_properties) > 1:
                message = InfoMessage(mcu=convert_str_to_enum(mcu_properties[0], SupportedMCU),
                                      prog_voltage_type=convert_str_to_enum(mcu_properties[1], ProgVoltages),
                                      non_blank_bytes=int(response[response.index('nonblank') + 1]),
                                      byte_cursor=int(response[response.index('counter') + 1]))
            elif len(mcu_properties) == 1:
                return Ecode.CHIP_NOT_FOUND
            else:
                return Ecode.UNKNOWN_CHIP
        except Exception as ex:
            logger.error(f'Generation chip info message failed: {ex}.')
            return Ecode.GENERATE_INFO_MESSAGE_FAILED
        else:
            return message

    @is_connected
    @check_chip
    @disconnect_if_error
    def get_pgm(self) -> Union[PGMMessage, Ecode]:
        return self._get_pgm()

    def _get_pgm(self) -> Union[PGMMessage, Ecode]:
        try:
            response = send_data(self._dev, Commands.GET_PGM_PARAMS)
        except Exception as ex:
            logger.error(f'Error getting chip pgm information: {ex}.')
            return Ecode.GETTING_PGM_DATA_FAILED

        try:
            params = response.split()[0].split(',')
            message = PGMMessage(mcu_postfix=int(params[0]), non_blank_bytes=int(params[1]), byte_cursor=int(params[2]))
        except Exception as ex:
            logger.error(f'Generation chip pgm message failed: {ex}.')
            return Ecode.GENERATE_PGM_MESSAGE_FAILED
        else:
            return message

    @is_connected
    @check_chip
    @disconnect_if_error
    def get_checksum(self) -> Union[int, Ecode]:
        return self._get_checksum()

    def _get_checksum(self) -> Union[int, Ecode]:
        try:
            response = send_data(self._dev, Commands.GET_CHECKSUM)
        except Exception as ex:
            logger.error(f'Error getting chip pgm information: {ex}.')
            return Ecode.GETTING_CHECKSUM_FAILED
        try:
            response = response.split()
            checksum = int(response[response.index('CHKSUM') + 2], 16)
        except Exception as ex:
            logger.error(f'Processing checksum data failed: {ex}.')
            return Ecode.CHECKSUM_PROCESSING_ERROR
        else:
            return checksum

    @is_connected
    @check_chip
    @disconnect_if_error
    def set_cursor(self, position: int) -> Ecode:
        return self._set_cursor(position)

    def _set_cursor(self, position: int) -> Ecode:
        try:
            counter = convert_counter(position)
            response = send_data(self._dev, Commands.SET_COUNTER, counter)
        except Exception as ex:
            logger.error(f'Set byte cursor failed: {ex}.')
            return Ecode.SET_CURSOR_FAILED
        else:
            logger.debug(f'Converted counter: {counter}.')
            logger.debug(f'Set counter response: {response}')
            return Ecode.OK

    @is_connected
    @check_chip
    @disconnect_if_error
    def erase(self) -> Ecode:
        return self._erase()

    def _erase(self) -> Ecode:
        try:
            response = send_data(self._dev, Commands.ERASE_FLASH)
        except Exception as ex:
            logger.error(f'Erase chip failed: {ex}.')
            return Ecode.ERASING_FAILED
        else:
            logger.debug(f'Erase response: {response}')
            return Ecode.OK

    @is_connected
    @check_chip
    @disconnect_if_error
    def write(self, path: str) -> Ecode:
        return self._write(path)

    def _write(self, hex_path: str) -> Ecode:
        hex_str = load_hex(hex_path)
        if not isinstance(hex_str, bytes):
            return hex_str

        print(f'Data length: {len(hex_str)}')
        ecode = self._set_cursor(len(hex_str))
        if ecode != Ecode.OK:
            return ecode
        print(f'Erase chip.')
        ecode = self._erase()
        if ecode != Ecode.OK:
            return ecode

        print(f'Write data.')
        try:
            response = send_data(self._dev, Commands.LOAD_FIRMWARE, hex_str, action_check=True)
        except Exception as ex:
            logger.error(f'Write hex to chip failed: {ex}.')
            return Ecode.WRITING_FAILED
        else:
            logger.debug(f'Write response: {response}')

        print(f'Verify.')
        return self._verify(hex_str)

    @is_connected
    @check_chip
    @disconnect_if_error
    def read(self, path: str):
        mcu_data = self._read()
        return save_hex(path, mcu_data)

    def _read(self, cursor: int = None) -> Union[bytes, Ecode]:
        info = self._get_info()
        if not isinstance(info, InfoMessage):
            return info

        memorysize = cursor if isinstance(cursor, int) else MCUMemorySize.get(info.mcu)
        ecode = self._set_cursor(memorysize)
        if ecode != Ecode.OK:
            return ecode

        try:
            response = send_data(self._dev, Commands.READ_FIRMWARE)
            response = bytes.fromhex(response)
        except Exception as ex:
            logger.error(f'Read binary string from chip failed: {ex}.')
            return Ecode.READING_FAILED
        else:
            return response

    @is_connected
    @check_chip
    def verify(self, path: str):
        return self._verify(path)

    def _verify(self, hex_obj: Union[str, bytes]) -> Ecode:
        if isinstance(hex_obj, str):
            hex_obj = load_hex(hex_obj)
        if not isinstance(hex_obj, bytes):
            return hex_obj

        mcu_data = self._read(len(hex_obj))
        if mcu_data == hex_obj:
            return Ecode.OK
        else:
            return Ecode.EMPTY_ARGUMENT
