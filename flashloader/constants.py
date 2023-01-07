from enum import Enum, auto


class Ecode(int, Enum):
    OK = auto()
    FILE_NOT_EXIST = auto()
    SAVING_FILE_ERROR = auto()
    EMPTY_ARGUMENT = auto()
    PROCESSING_ARGUMENT_FAILED = auto()
    PROGRAMMER_DISCONNECTED = auto()
    CONNECTION_ERROR = auto()
    DISCONNECTION_ERROR = auto()
    HEX_PROCESSING_ERROR = auto()
    CHECKSUM_PROCESSING_ERROR = auto()
    SET_CURSOR_FAILED = auto()
    ERASING_FAILED = auto()
    WRITING_FAILED = auto()
    READING_FAILED = auto()
    GETTING_CHECKSUM_FAILED = auto()
    GETTING_PGM_DATA_FAILED = auto()
    GETTING_INFO_DATA_FAILED = auto()
    GETTING_TITLE_FAILED = auto()
    GENERATE_COUNTER_DATA_FAILED = auto()
    GENERATE_PGM_MESSAGE_FAILED = auto()
    GENERATE_INFO_MESSAGE_FAILED = auto()
    UNKNOWN_CHIP = auto()
    CHIP_NOT_FOUND = auto()


class ProgVoltages(str, Enum):
    LOW = '5V'
    HIGH = '12V'


class SupportedMCU(str, Enum):
    AT89C51 = '89C51'
    AT89C52 = '89C52'
    AT89C55 = '89C55'


MCUMemorySize = {
    SupportedMCU.AT89C51: 4096,
    SupportedMCU.AT89C52: 8192,
    SupportedMCU.AT89C55: 20480,
}
