
from typing import Iterable, Tuple, Any
from .b334 import b334
from ..constants import *
from ..types import *
from ..io import *

class b338(b334):
    """
    b338 changes the structure of statuses & stats.
    """
    version = 338

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_u8(stream, Completeness.Statistics)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u16(stream, info.stats.rank)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_u8(stream, Completeness.Full)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u16(stream, info.stats.rank)
        write_string(stream, info.name)
        write_string(stream, info.avatar_filename)
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.country_string)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        stream = MemoryStream()
        write_u8(stream, status.action)

        beatmap_update = True
        write_boolean(stream, beatmap_update)

        if beatmap_update:
            write_string(stream, status.text)
            write_string(stream, status.beatmap_checksum)
            write_u16(stream, status.mods)

        return stream.data

    @classmethod
    def read_user_status(cls, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = Status(read_u8(stream))
        beatmap_update = read_boolean(stream)

        if beatmap_update:
            status.text = read_string(stream)
            status.beatmap_checksum = read_string(stream)
            status.mods = Mods(read_u16(stream))

        if status.action == Status.Idle and status.beatmap_checksum:
            # There is a bug where the client starts playing but
            # doesn't set the status to "Playing".
            status.action = Status.Playing

        return status
