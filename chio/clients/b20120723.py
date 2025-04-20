
from typing import Iterable, Tuple
from .b20120703 import b20120703
from ..constants import *
from ..types import *
from ..io import *

class b20120723(b20120703):
    """
    b20120723 now shows your performance points in-game.
    """
    version = 20120723
    protocol_version = 8

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, info.id)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)

        if cls.protocol_version >= 8:
            write_s16(stream, info.stats.pp)

        yield PacketType.BanchoUserStats, stream.data
