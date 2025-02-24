
from typing import Iterable, Tuple
from .b470 import b470
from ..constants import *
from ..types import *
from ..io import *

class b487(b470):
    """
    b487 adds support for bancho protocol negotiations.
    """
    version = 487

    @classmethod
    def write_protocol_negotiation(cls, version: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, version)
        yield PacketType.BanchoProtocolNegotiation, stream.data
