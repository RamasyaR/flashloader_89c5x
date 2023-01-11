import logging
from typing import Optional, Type, Union

import serial

from ..constants import ProgVoltages, SupportedMCU
from .enums import ActionSignals, Commands

logger = logging.getLogger(__name__)


def convert_str_to_enum(string: str, concrete_enum: Union[Type[SupportedMCU],
                                                          Type[ProgVoltages]]) -> Optional[Union[SupportedMCU,
                                                                                                 ProgVoltages]]:
    if concrete_enum not in [SupportedMCU, ProgVoltages]:
        raise TypeError(f'Unexpected enum: {concrete_enum}')

    try:
        return concrete_enum(string)
    except (Exception, ):
        logger.warning(f'Unknown mcu property received: {string} , immediately remove the controller from the ZIF '
                       f'panel, there is a risk of damage.')
        return None


def convert_counter(count_num: int) -> bytes:
    if count_num < 0:
        raise ValueError(f'Invalid counter value: {count_num}, negative value')
    count_str = f'{count_num}\n'
    if len(count_str) > 6:
        raise ValueError(f'Too big value: {count_str}, no more than 5 digits were expected')
    return bytes(count_str, encoding='utf-8')


def cut_footer(data: str) -> str:
    return data.replace('\n\r ok\n\r >', '')


def send_data(dev: serial.Serial, command: Commands, data: bytes = None, action_check: bool = False) -> str:
    if not isinstance(command, Commands):
        raise ValueError(f'Expected single byte command, recieved: {command}')

    dev.flushInput()
    dev.flushOutput()

    send_byte(dev, command, False)

    if data:
        for idx in range(len(data)):
            wait_allow_byte(dev)
            send_byte(dev, data[idx:idx+1], action_check)

    data = dev.read_until(expected=b'>').decode(encoding='utf-8')
    return cut_footer(data)


def send_byte(dev: serial.Serial, byte: bytes, action_check):
    if not isinstance(byte, bytes) or len(byte) != 1:
        raise ValueError(f'Expected single byte, recieved: {byte}')
    dev.write(byte)
    response = dev.read(1)

    check_byte = ActionSignals.XOFF if action_check else byte

    if check_byte != response:
        logger.error(f'send != responce: {check_byte} != {response}.')
        # raise RuntimeError(f'send != responce')


def wait_allow_byte(dev: serial.Serial) -> None:
    byte = dev.read(1)
    if byte != ActionSignals.XON:
        logger.error(f'In waiting allow: {byte} != {ActionSignals.XON}.')
        # raise RuntimeError(f'byte != ActionSignals.XON')
