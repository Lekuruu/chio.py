
from typing import Iterable, Tuple
from .b695 import b695
from ..constants import *
from ..types import *
from ..io import *

class b1183(b695):
    """
    b1183 adds the longitude and latitude fields to user presence.
    """
    version = 1183
    protocol_version = 5

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
        write_u32(stream, info.stats.rank)
        write_string(stream, info.name)
        write_string(stream, info.avatar_filename)
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.country_string)
        write_u8(stream, info.presence.permissions)

        if cls.protocol_version >= 5:
            write_f32(stream, info.presence.longitude)
            write_f32(stream, info.presence.latitude)

        yield PacketType.BanchoUserStats, stream.data
