
from typing import Optional, Iterable, Tuple
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
    def write_protocol_negotiation(cls, version: Optional[int] = None) -> Iterable[Tuple[PacketType, bytes]]:
        # This lets us decide if we want to use the pre-defined
        # version or a custom version we can provide.
        stream = MemoryStream()
        write_s32(stream, version or cls.protocol_version)
        yield PacketType.BanchoProtocolNegotiation, stream.data
