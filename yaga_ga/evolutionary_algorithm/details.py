from typing import TypeVar, Any
from typing_extensions import Protocol

T = TypeVar("T")


class Comparable(Protocol):
    def __eq__(self: T, other: Any) -> bool:
        ...

    def __lt__(self: T, other: T) -> bool:
        ...
