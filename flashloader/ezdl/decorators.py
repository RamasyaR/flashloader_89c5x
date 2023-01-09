import functools
from typing import Any, Callable

from flashloader.constants import Ecode

from .messages import InfoMessage


def check_programmer(method) -> Callable:
    @functools.wraps(method)
    def foo(self, *args, **kwargs) -> Any:
        if self._is_connected():
            return method(self, *args, **kwargs)
        else:
            return Ecode.PROGRAMMER_DISCONNECTED
    return foo


def check_chip(method) -> Callable:
    @functools.wraps(method)
    def foo(self, *args, **kwargs) -> Any:
        info = self._get_info()
        if not isinstance(info, InfoMessage):
            return info
        return method(self, *args, **kwargs)
    return foo
