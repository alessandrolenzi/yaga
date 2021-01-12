from typing import TypeVar, Protocol, Any

T = TypeVar("T")


class Comparable(Protocol):
    def __eq__(self: T, other: Any) -> bool:
        ...

    def __lt__(self: T, other: T) -> bool:
        ...
