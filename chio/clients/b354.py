
from typing import Iterable, Tuple
from .b349 import b349
from ..constants import *
from ..types import *
from ..io import *

class b354(b349):
    """
    b354 adds the beatmap info packets.
    """
    version = 354

    @classmethod
    def read_beatmap_info_request(cls, stream: MemoryStream) -> BeatmapInfoRequest:
        return BeatmapInfoRequest([read_string(stream) for _ in range(read_u32(stream))])

    @classmethod
    def write_beatmap_info_reply(cls, reply: BeatmapInfoReply) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, len(reply.beatmaps))

        for info in reply.beatmaps:
            write_s16(stream, info.index)
            write_s32(stream, info.beatmap_id)
            write_s32(stream, info.beatmapset_id)
            write_s32(stream, info.thread_id)
            write_boolean(stream, info.is_ranked)
            write_s8(stream, info.osu_rank)
            write_string(stream, info.checksum)

        yield PacketType.BanchoBeatmapInfoReply, stream.data
