"""
http://www.aprs-is.net/javAPRSFilter.aspx
"""
import dataclasses
import enum
from typing import ClassVar, List, Optional

from .models import Point, Types


@dataclasses.dataclass
class Filter:
    """
    Base filter

    Users can bitwise invert the class to negate the filter:
    >>> str(RangeFilter(123, -123, 15)) == "r/123/-123/15"
    >>> str(~RangeFilter(123, -123, 15)) == "-r/123/-123/15"
    """
    _inverse: bool = dataclasses.field(default=False, init=False)

    def __invert__(self):
        self._inverse = True
        return self

    def __str__(self):
        if self._inverse:
            return "-"
        return ""


@dataclasses.dataclass
class RangeFilter(Filter):
    point: Point
    radius: float  # km

    def __str__(self) -> str:
        return super().__str__() + f"r/{self.point.latitude}/{self.point.longitude}/{self.radius}"


@dataclasses.dataclass
class ListItemFilter(Filter):
    prefix: ClassVar[str] = None

    items: List[str]

    def __str__(self):
        return super().__str__() + f"{self.prefix}/" + "/".join(self.items)


class PrefixFilter(ListItemFilter):
    prefix = "p"


class BudlistFilter(ListItemFilter):
    prefix = "b"


class ObjectFilter(ListItemFilter):
    prefix  = "o"


class StrictObjectFilter(ListItemFilter):
    prefix  = "os"


@dataclasses.dataclass
class TypeFilter(Filter):
    items: List[Types]
    call: Optional[str] = None
    radius: Optional[float] = None

    def __str__(self):
        base = super().__str__() + f"t/" + "".join((x.value for x in self.items))
        if self.call:
            base += "/" + self.call
        if self.radius:
            base += "/" + str(self.radius)
        return base


@dataclasses.dataclass
class AreaFilter(Filter):
    nw_point: Point
    se_point: Point

    def __str__(self):
        return (
            super().__str__() +
            f"a/{self.nw_point.latitude}/{self.nw_point.longitude}" +
            f"/{self.se_point.latitude}/{self.se_point.longitude}"
        )
