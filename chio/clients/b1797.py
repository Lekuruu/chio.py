
from typing import Iterable, Tuple
from .b1796 import b1796
from ..constants import *
from ..types import *
from ..io import *

class b1797(b1796):
    """
    b1797 adds the rank field to re-enable user rank sorting.
    """
    version = 1797
    protocol_version = 7

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, cls.convert_user_id(info))
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
