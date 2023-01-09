import glob
import logging
import os
import shlex
from typing import List, Union

from flashloader.constants import Ecode

logger = logging.getLogger(__name__)


def path_completion(text, line, _, endidx) -> List[str]:
    try:
        split = None
        for quote in ['', '"', "'"]:
            try:
                split = [s for s in shlex.split(line[:endidx] + quote) if s.strip()]
            except (Exception, ):
                continue
            break

        if split is None:
            return []
        glob_prefix = os.path.expanduser(split[-1] if len(split) > 1 else '')
        cutoff_idx = len(glob_prefix) - len(text)
        return [match[cutoff_idx:] + os.sep if os.path.isdir(match) else match[cutoff_idx:]
                for match in glob.glob(glob_prefix + '*')]
    except (Exception, ):
        return []


def parse_arg(arg: str, expected_type: type = str) -> Union[str, int, float, Ecode]:
    if not len(arg):
        return Ecode.EMPTY_ARGUMENT

    try:
        if expected_type is str:
            if arg[0] == "\'" and arg[-1] == "\'":
                arg = arg[1:-1]
        else:
            arg = expected_type(arg)
    except Exception as ex:
        logger.error(f'Error processing input argument: {ex}.')
        return Ecode.PROCESSING_ARGUMENT_FAILED
    else:
        return arg


def handle_ecode(ecode: Ecode) -> str:
    if isinstance(ecode, Ecode):
        return str(ecode.value)
    else:
        return f'Unexpected error {ecode}, sorry.'
