
from typing import Iterable, Tuple
from .b20121023 import b20121023
from ..constants import *
from ..types import *
from ..io import *

class b20121028(b20121023):
    """
    b20121028 adds the osu! mania ranking field to the beatmap info packet.
    """
    version = 20121028
    protocol_version = 12

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
            write_s8(stream, info.fruits_rank)
            write_s8(stream, info.taiko_rank)

            if cls.protocol_version >= 12:
                write_s8(stream, info.mania_rank)

            write_string(stream, info.checksum)

        yield PacketType.BanchoBeatmapInfoReply, stream.data
