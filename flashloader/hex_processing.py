import logging
import os
from typing import Union

from intelhex import IntelHex

from .constants import Ecode

logger = logging.getLogger(__name__)


def load_hex(path: str) -> Union[bytes, Ecode]:
    try:
        if not os.path.exists(path):
            return Ecode.FILE_NOT_EXIST
    except Exception as ex:
        logger.error(f'Error check file existing: {ex}.')
        return Ecode.PROCESSING_ARGUMENT_FAILED

    try:
        ih = IntelHex()
        ih.loadhex(path)
        binstr = ih.tobinstr()
    except Exception as ex:
        logger.error(f'Processing hex data failed: {ex}.')
        return Ecode.HEX_PROCESSING_ERROR
    else:
        return binstr


def save_hex(path: str, binstr: bytes) -> Ecode:
    try:
        ih = IntelHex()
        ih.frombytes(binstr)
        ih = remove_padding_bytes(ih)
    except Exception as ex:
        logger.error(f'Processing hex data failed: {ex}.')
        return Ecode.HEX_PROCESSING_ERROR

    try:
        with open(path, 'w') as file:
            ih.tofile(file, format='hex')
    except Exception as ex:
        logger.error(f'Saving hex file failed: {ex}.')
        return Ecode.SAVING_FILE_ERROR
    else:
        return Ecode.OK


def remove_padding_bytes(ih: IntelHex) -> IntelHex:
    ih_dict = {k: v for k, v in ih.todict().items() if v != 0xFF}
    return IntelHex(ih_dict)
