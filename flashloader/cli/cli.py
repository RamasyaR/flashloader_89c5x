import logging
from cmd import Cmd

from flashloader.constants import Ecode
from flashloader.ezdl import EZDLFlasher, InfoMessage, PGMMessage

from .utils import handle_ecode, parse_arg, path_completion

logger = logging.getLogger('flasher')


class FlasherCLI(EZDLFlasher, Cmd):
    intro = 'Welcome to the flashtool shell. Type help or ? to list commands.\n'
    prompt = 'flasher > '

    def __init__(self):
        EZDLFlasher.__init__(self)
        Cmd.__init__(self)

    def do_connect(self, arg: str) -> None:
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(f'{handle_ecode(arg)} Expected device path, like /dev/ttyUSB0.')
            return

        title = self.connect(arg)
        if isinstance(title, str):
            print(f'Successfully connected to {arg}.\n'
                  f'{title}')
        elif title == Ecode.OK:
            print('Programmer is already connected.')
        else:
            print(f'Connect to {arg} failed: {handle_ecode(title)}')

    def do_disconnect(self, _) -> None:
        ecode = self.disconnect()
        if ecode != Ecode.OK:
            print(f'Disconnecting finish with error: {handle_ecode(ecode)}')
        else:
            print(f'Successfully disconnected.')

    def do_status(self, _) -> None:
        dev = self.device
        if dev is not None:
            print(f'Programmer connected on {dev}.')
        else:
            print(f'Programmer is not connected.')

    def do_programmer_info(self, _) -> None:
        title = self.get_title()
        message = title if isinstance(title, str) else handle_ecode(title)
        print(message)

    def do_chip_info(self, _) -> None:
        result = self.get_info()
        if isinstance(result, InfoMessage):
            print(f'\nChip: {result.mcu}\n'
                  f'Programming voltage: {result.prog_voltage_type}\n'
                  f'Non blank memory bytes: {result.non_blank_bytes}\n')
        else:
            print(handle_ecode(result))

    def do_get_pgm(self, _) -> None:
        result = self.get_pgm()
        if isinstance(result, PGMMessage):
            print(f'Getting PGM completed successfully: {result}.')
        else:
            print(handle_ecode(result))

    def do_get_checksum(self, _) -> None:
        result = self.get_checksum()
        if isinstance(result, Ecode):
            print(handle_ecode(result))
        else:
            print(f'Getting checksum completed successfully: {result}.')

    def do_set_cursor(self, arg: str) -> None:
        arg = parse_arg(arg, expected_type=int)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.set_cursor(arg)
        if ecode != Ecode.OK:
            print(f'Set {arg} failed: {handle_ecode(ecode)}')
        else:
            print(f'Set byte cursor {arg} completed successfully.')

    def do_erase(self, _) -> None:
        ecode = self.erase()
        if ecode != Ecode.OK:
            print(handle_ecode(ecode))
        else:
            print(f'Erasing completed successfully.')

    def do_write(self, arg: str) -> None:
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.write(arg)
        if ecode != Ecode.OK:
            print(handle_ecode(ecode))
        else:
            print(f'Writing completed successfully.')

    def do_read(self, arg: str):
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.read(arg)
        if ecode != Ecode.OK:
            print(handle_ecode(ecode))
        else:
            print(f'Reading memory completed successfully.')

    def do_verify(self, arg: str):
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.verify(arg)
        if ecode != Ecode.OK:
            print(handle_ecode(ecode))
        else:
            print(f'Verify memory completed successfully.')

    @staticmethod
    def do_exit(_):
        """Stop recording, close the flasher window, and exit."""
        print('Thank you for using flashtool.')
        return True

    @staticmethod
    def complete_connect(text, line, startidx, endidx):
        return path_completion(text, line, startidx, endidx)

    @staticmethod
    def complete_write(text, line, startidx, endidx):
        return path_completion(text, line, startidx, endidx)

    @staticmethod
    def complete_read(text, line, startidx, endidx):
        return path_completion(text, line, startidx, endidx)

    @staticmethod
    def complete_verify(text, line, startidx, endidx):
        return path_completion(text, line, startidx, endidx)
