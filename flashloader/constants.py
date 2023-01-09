from enum import Enum, auto


class Ecode(str, Enum):
    OK = 'Command completed successfully.'
    FILE_NOT_EXIST = 'Invalid file path, file not exist.'
    SAVING_FILE_ERROR = auto()
    EMPTY_ARGUMENT = 'Argument expected but not passed.'
    PROCESSING_ARGUMENT_FAILED = 'Error processing input argument.'
    PROGRAMMER_DISCONNECTED = 'Programmer is not connected.'
    CONNECTION_ERROR = 'Connecting to flasher programmer failed, replug your device.'
    DISCONNECTION_ERROR = 'Disconnecting finish with error.'
    HEX_PROCESSING_ERROR = 'Error processing hex file, check your binary file.'
    CHECKSUM_PROCESSING_ERROR = 'Error processing checksum message.'
    SET_CURSOR_FAILED = 'Set byte cursor finsh with error.'
    ERASING_FAILED = 'Erasing chip memory failed'
    WRITING_FAILED = 'Writing hex file to chip memory failed.'
    READING_FAILED = 'Reading chip memory finished with error.'
    VERIFICATION_FAILED = auto()
    GETTING_CHECKSUM_FAILED = 'Error getting checksum from chip.'
    GETTING_PGM_DATA_FAILED = 'Error getting pgm data from chip.'
    GETTING_INFO_DATA_FAILED = 'Error getting programmer information.'
    GETTING_TITLE_FAILED = auto()
    GENERATE_COUNTER_DATA_FAILED = 'Generating counter message for programmer failed, invalid counter value.'
    GENERATE_PGM_MESSAGE_FAILED = 'Error parse PGM message from programmer.'
    GENERATE_INFO_MESSAGE_FAILED = 'Error parse chip information message from programmer.'
    UNKNOWN_CHIP = 'Failed to recognize the chip.'
    CHIP_NOT_FOUND = 'Chip not found.'


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
