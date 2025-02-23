
from typing import Iterable, Tuple
from .b354 import b354
from ..constants import *
from ..types import *
from ..io import *

class b388(b354):
    """
    b388 changes ranked status from bool->int in beatmap info packets.
    """
    version = 388
    
    @classmethod
    def write_beatmap_info_reply(cls, reply: BeatmapInfoReply) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, len(reply.beatmaps))

        for info in reply.beatmaps:
            write_s16(stream, info.index)
            write_s32(stream, info.beatmap_id)
            write_s32(stream, info.beatmapset_id)
            write_s32(stream, info.thread_id)
            write_s8(stream, info.ranked_status)
            write_s8(stream, info.osu_rank)
            write_string(stream, info.checksum)

        yield PacketType.BanchoBeatmapInfoReply, stream.data
