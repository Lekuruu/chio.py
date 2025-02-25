
from typing import Iterable, Tuple
from .b1796 import b1796
from ..constants import *
from ..types import *
from ..io import *

class b1797(b1796):
    """
    b1796
    """
    version = 1797
    protocol_version = 7

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        # User IDs are negative if they are IRC users
        user_id = (
            abs(info.id) if not info.presence.is_irc else
            -abs(info.id)
        )

        write_u32(stream, user_id)
        write_string(stream, info.name)
        write_u8(stream, AvatarExtension.Png)
        write_u8(stream, info.presence.timezone+24)
        write_u8(stream, info.presence.country_index)
        write_string(stream, info.presence.city)
        write_u8(stream, info.presence.permissions)
        write_f32(stream, info.presence.longitude)
        write_f32(stream, info.presence.latitude)

        if cls.protocol_version >= 7:
            write_s32(stream, info.stats.rank)

        yield PacketType.BanchoUserPresence, stream.data
