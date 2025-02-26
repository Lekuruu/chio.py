
from typing import Iterable, Tuple
from .b20120818 import b20120818
from ..constants import *
from ..types import *
from ..io import *

class b20121023(b20120818):
    """
    b20121023 adds the "ban/silence info" packet, which locks down account switching
    on the client-side, and tells the user how long they are banned/silenced for.
    """
    version = 20121023
    protocol_version = 11

    @classmethod
    def write_silence_info(cls, length_seconds: int = -1) -> Iterable[Tuple[PacketType, bytes]]:
        # NOTE: If set to "-1", the client will reset the silence
        #       info and allow account switching again.
        stream = MemoryStream()
        write_s32(stream, length_seconds)
        yield PacketType.BanchoSilenceInfo, stream.data
