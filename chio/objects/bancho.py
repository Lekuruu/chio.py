
from chio.streams import StreamIn

from dataclasses import dataclass
from typing import Any
from enum import Enum

@dataclass
class BanchoPacket:
    packet: Enum
    compression: bool
    data: Any
