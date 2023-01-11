import glob
import logging
import os
import shlex

try:
    import readline
except ImportError:
    readline = None

from typing import List, Optional, Union

from serial.tools.list_ports import comports

from flashloader.constants import Ecode

logger = logging.getLogger(__name__)


def load_history(path: str) -> None:
    if readline:
        expanded_path = os.path.expanduser(path)
        if not os.path.exists(expanded_path):
            return
        readline.read_history_file(expanded_path)


def save_history(path: str, size: int) -> None:
    if readline:
        expanded_path = os.path.expanduser(path)
        history_dir = os.path.dirname(expanded_path)
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        readline.set_history_length(size)
        readline.write_history_file(expanded_path)


def com_port_completion(text, line, _, endidx) -> List[str]:
    try:
        split = _split_args(line, endidx)
        raw_path = _join_path(split)
        if raw_path is None:
            return []
        cutoff_idx = len(raw_path) - len(text)
        return [port.device[cutoff_idx:] for port in comports(include_links=True) if raw_path in port.device]
    except (Exception, ):
        return []


def path_completion(text, line, _, endidx):
    try:
        split = _split_args(line, endidx)
        raw_path = _join_path(split)
        if raw_path is None:
            return []
        glob_prefix = os.path.expanduser(raw_path)
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


def _join_path(split_path: List[str]) -> Optional[str]:
    split_len = len(split_path)
    if split_len == 1:
        return ''
    elif split_len == 2:
        return split_path[-1]
    elif split_len > 2:
        return ' '.join(split_path[1:])
    else:
        return None


def _split_args(raw_arg: str, endidx: int) -> List[str]:
    split = []
    for idx, quote in enumerate(['', '"', "'"]):
        try:
            split.extend(shlex.split(raw_arg[:endidx] + quote))
        except (Exception,):
            continue
        else:
            break
    return split
