
from typing import Iterable, Tuple
from .b20140716 import b20140716
from ..constants import *
from ..types import *
from ..io import *

class b20140731(b20140716):
    """
    b20140731 adds the infamous "Zallius' eyes have awoken" (RTX) packet.
    """
    version = 20140731

    @classmethod
    def write_rtx(cls, message: str = "Zallius' eyes have awoken") -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message)
        yield PacketType.BanchoRTX, stream.data
