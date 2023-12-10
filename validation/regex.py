import re
from typing import Callable

from typeguard import typechecked


@typechecked
def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))
    res._name_ = f'pattern({regex})'
    return res
