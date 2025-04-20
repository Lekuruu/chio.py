
from typing import Iterable, Tuple
from .b20161101 import b20161101
from ..constants import *
from ..types import *
from ..io import *

class b20250306(b20161101):
    """
    b20250306 changes the pp datatype from s16 to u16, due
    to mrekk exceeding the integer limit.
    https://osu.ppy.sh/home/changelog/stable40/20250306.2
    https://www.reddit.com/r/osugame/comments/1j3y7fh/
    """
    version = 20250306

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
        write_u16(stream, info.stats.pp)
        yield PacketType.BanchoUserStats, stream.data
