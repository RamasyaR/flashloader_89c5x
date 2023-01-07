import functools
from typing import Any, Callable

from flashloader.constants import Ecode

from .messages import InfoMessage


def is_connected(method) -> Callable:
    @functools.wraps(method)
    def foo(self, *args, **kwargs) -> Any:
        if self._is_connected():
            return method(self, *args, **kwargs)
        else:
            return Ecode.PROGRAMMER_DISCONNECTED
    return foo


def disconnect_if_error(method) -> Callable:
    @functools.wraps(method)
    def foo(self, *args, **kwargs) -> Any:
        result = method(self, *args, **kwargs)
        if isinstance(result, Ecode) and result != Ecode.OK:
            self.disconnect()
        return result
    return foo


def check_chip(method) -> Callable:
    @functools.wraps(method)
    def foo(self, *args, **kwargs) -> Any:
        info = self.get_info()
        if not isinstance(info, InfoMessage):
            return info
        return method(self, *args, **kwargs)
    return foo
