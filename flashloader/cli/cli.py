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
            message = f'Successfully connected to {arg}.\n' \
                      f'{title}'
        elif title == Ecode.OK:
            message = 'Programmer is already connected.'
        else:
            message = f'Connect to {arg} failed: {handle_ecode(title)}'
        print(message)

    def do_disconnect(self, _) -> None:
        ecode = self.disconnect()
        message = 'Successfully disconnected.' if ecode == Ecode.OK \
            else f'Disconnecting finish with error: {handle_ecode(ecode)}'
        print(message)

    def do_status(self, _) -> None:
        dev = self.device
        message = f'Programmer connected on {dev}.' if dev is not None else 'Programmer is not connected.'
        print(message)

    def do_programmer_info(self, _) -> None:
        title = self.get_title()
        message = title if isinstance(title, str) else handle_ecode(title)
        print(message)

    def do_chip_info(self, _) -> None:
        result = self.get_info()
        if isinstance(result, InfoMessage):
            message = f'\n' \
                      f'Chip: {result.mcu}\n' \
                      f'Programming voltage: {result.prog_voltage_type}\n' \
                      f'Non blank memory bytes: {result.non_blank_bytes}\n'
        else:
            message = handle_ecode(result)
        print(message)

    def do_get_pgm(self, _) -> None:
        result = self.get_pgm()
        message = f'Getting PGM completed successfully: {result}.' if isinstance(result, PGMMessage) \
            else handle_ecode(result)
        print(message)

    def do_get_checksum(self, _) -> None:
        result = self.get_checksum()
        message = f'Getting checksum completed successfully: {result}.' if not isinstance(result, Ecode) \
            else handle_ecode(result)
        print(message)

    def do_set_cursor(self, arg: str) -> None:
        arg = parse_arg(arg, expected_type=int)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.set_cursor(arg)
        message = f'Set byte cursor {arg} completed successfully.' if ecode == Ecode.OK \
            else f'Set {arg} failed: {handle_ecode(ecode)}'
        print(message)

    def do_erase(self, _) -> None:
        ecode = self.erase()
        message = 'Erasing completed successfully.' if ecode == Ecode.OK else handle_ecode(ecode)
        print(message)

    def do_write(self, arg: str) -> None:
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.write(arg)
        message = 'Writing completed successfully.' if ecode == Ecode.OK else handle_ecode(ecode)
        print(message)

    def do_read(self, arg: str):
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.read(arg)
        message = 'Reading memory completed successfully.' if ecode == Ecode.OK else handle_ecode(ecode)
        print(message)

    def do_verify(self, arg: str):
        arg = parse_arg(arg)
        if isinstance(arg, Ecode):
            print(handle_ecode(arg))
            return

        ecode = self.verify(arg)
        message = 'Verify memory completed successfully.' if ecode == Ecode.OK else handle_ecode(ecode)
        print(message)

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
