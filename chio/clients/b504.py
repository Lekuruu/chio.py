
from typing import Iterable, Tuple
from .b490 import b490
from ..constants import *
from ..types import *
from ..io import *

class b504(b490):
    """
    b504 adds the taiko & fruits ranks to the beatmap info packet.
    """
    version = 504
    protocol_version = 2

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

            if cls.protocol_version >= 2:
                write_s8(stream, info.fruits_rank)
                write_s8(stream, info.taiko_rank)

            write_string(stream, info.checksum)

        yield PacketType.BanchoBeatmapInfoReply, stream.data

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        # NOTE: See b365 for the level overflow bug
        write_u32(stream, info.id)
        write_u8(stream, Completeness.Statistics)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, min(info.stats.tscore, 26931190827))
        write_u16(stream, info.stats.rank)
        yield PacketType.BanchoUserStats, stream.data
    
    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        # NOTE: See b365 for the level overflow bug
        write_u32(stream, info.id)
        write_u8(stream, Completeness.Full)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, min(info.stats.tscore, 26931190827))
        write_u16(stream, info.stats.rank)
        write_string(stream, info.name)
        write_string(stream, info.avatar_filename)
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.country_string)
        write_u8(stream, info.presence.permissions)
        yield PacketType.BanchoUserStats, stream.data
