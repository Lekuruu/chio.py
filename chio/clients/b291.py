
from typing import Iterable, Tuple
from ..types import PacketType
from .b282 import b282
from ..io import *

class b291(b282):
    """
    b291 implements the GetAttension & Announce packets.
    """
    @classmethod
    def write_get_attention(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoGetAttention, b''

    @classmethod
    def write_announce(cls, message: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message)
        yield PacketType.BanchoAnnounce, stream.data
