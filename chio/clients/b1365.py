
from typing import Iterable, Tuple
from .b1183 import b1183
from ..constants import *
from ..types import *
from ..io import *

class b1365(b1183):
    """
    b1365 now sends "player skipped" messages in multiplayer.
    """
    version = 1365

    @classmethod
    def write_match_player_skipped(cls, slot_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, slot_id)
        yield PacketType.BanchoMatchPlayerSkipped, stream.data
