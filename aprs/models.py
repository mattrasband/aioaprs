import dataclasses
import enum
from typing import List

import aprslib


@dataclasses.dataclass(frozen=True)
class Point:
    """
    A lat/lon point (in decimal degrees)
    """
    latitude: float
    longitude: float


@enum.unique
class Types(enum.Enum):
    ITEMS = "i"
    MESSAGE = "m"
    NWS = "n"
    OBJECTS = "o"
    POSITION = "p"
    QUERY = "q"
    STATUS = "s"
    TELEMETRY = "t"
    USER_DEFINED = "u"
    WEATHER = "w"
