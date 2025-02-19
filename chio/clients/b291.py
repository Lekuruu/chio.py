
from typing import Iterable, Tuple
from ..types import PacketType
from .b282 import b282
from ..io import *

class b291(b282):
    """
    b291 implements the GetAttension & Announce packets.
    """
    def write_get_attension(self) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.GetAttension, b''

    def write_announce(self, message: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message)
        yield PacketType.Announce, stream.data
