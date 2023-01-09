from enum import Enum


class Commands(bytes, Enum):
    GET_TITLE = b'\n'
    GET_INFO = b'g'
    GET_PGM_PARAMS = b'p'
    GET_CHECKSUM = b'c'
    GET_HELP = b'?'

    ERASE_FLASH = b'e'
    LOAD_FIRMWARE = b'w'
    READ_FIRMWARE = b'r'
    LOCK_FLASH = b'l'

    SET_COUNTER = b's'


class ActionSignals(bytes, Enum):
    XON = b'\x11'
    XOFF = b'\x13'
