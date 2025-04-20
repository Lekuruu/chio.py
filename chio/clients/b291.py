
from typing import Iterable, Tuple
from ..types import PacketType
from .b282 import b282
from ..io import *

class b291(b282):
    """
    b291 implements the GetAttension & Announce packets.
    """
    version = 291

    @classmethod
    def write_get_attention(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoGetAttention, b''

    @classmethod
    def write_announce(cls, message: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message)
        yield PacketType.BanchoAnnounce, stream.data

    @classmethod
    def write_restart(cls, retry_after_ms: int = 5000) -> Iterable[Tuple[PacketType, bytes]]:
        # NOTE: This is a backport of the actual restart packet, that
        #       simply announces the server restart to the user.
        return cls.write_announce(f"Bancho is restarting, please wait...")
