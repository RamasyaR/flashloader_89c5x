from flashloader.constants import Ecode

ECODE_MESSAGES = {
    Ecode.OK: 'Command completed successfully.',
    Ecode.EMPTY_ARGUMENT: 'Argument expected but not passed.',
    Ecode.PROCESSING_ARGUMENT_FAILED: 'Error processing input argument.',
    Ecode.PROGRAMMER_DISCONNECTED: 'Programmer is not connected.',
    Ecode.CONNECTION_ERROR: 'Connecting to flasher programmer failed, replug your device.',
    Ecode.DISCONNECTION_ERROR: 'Disconnecting finish with error.',
    Ecode.HEX_PROCESSING_ERROR: 'Error processing hex file, check your binary file.',
    Ecode.CHECKSUM_PROCESSING_ERROR: 'Error processing checksum message.',
    Ecode.SET_CURSOR_FAILED: 'Set byte cursor finsh with error.',
    Ecode.ERASING_FAILED: 'Erasing chip memory failed',
    Ecode.WRITING_FAILED: 'Writing hex file to chip memory failed.',
    Ecode.GETTING_CHECKSUM_FAILED: 'Error getting checksum from chip.',
    Ecode.GETTING_PGM_DATA_FAILED: 'Error getting pgm data from chip.',
    Ecode.GETTING_TITLE_FAILED: 'Error getting programmer information.',
    Ecode.GENERATE_COUNTER_DATA_FAILED: 'Generating counter message for programmer failed, invalid counter value.',
    Ecode.GENERATE_PGM_MESSAGE_FAILED: 'Error parse PGM message from programmer.',
    Ecode.GENERATE_INFO_MESSAGE_FAILED: 'Error parse chip information message from programmer.',
    Ecode.UNKNOWN_CHIP: 'Failed to recognize the chip.',
    Ecode.CHIP_NOT_FOUND: 'Chip not found.',

}
