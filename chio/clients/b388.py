
from typing import Iterable, Tuple, Union
from .b374 import b374
from ..constants import *
from ..types import *
from ..io import *

class b388(b374):
    """
    b388 changes ranked status from bool->int in beatmap info packets.
    """
    version = 388

    @classmethod
    def convert_ranked_status(cls, status: Union[RankedStatus, int]) -> int:
        if type(status) is int:
            # A custom status was sent
            return status

        # Approved status does not exist
        status_mapping = {
            RankedStatus.NotSubmitted: -1,
            RankedStatus.Pending: 0,
            RankedStatus.Ranked: 1,
            RankedStatus.Approved: 2,
            RankedStatus.Qualified: 2,
            RankedStatus.Loved: 2
        }
        return status_mapping.get(status, -1)

    @classmethod
    def write_beatmap_info_reply(cls, reply: BeatmapInfoReply) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, len(reply.beatmaps))

        for info in reply.beatmaps:
            write_s16(stream, info.index)
            write_s32(stream, info.beatmap_id)
            write_s32(stream, info.beatmapset_id)
            write_s32(stream, info.thread_id)
            write_s8(stream, cls.convert_ranked_status(info.ranked_status))
            write_s8(stream, info.osu_rank)
            write_string(stream, info.checksum)

        yield PacketType.BanchoBeatmapInfoReply, stream.data
