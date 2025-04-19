
from typing import Iterable, Tuple
from .b20120725 import b20120725
from ..constants import *
from ..types import *
from ..io import *

class b20120806(b20120725):
    """
    b20120806 adds the current user's mode to the presence packet.
    """
    version = 20120806
    protocol_version = 10

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

        if cls.protocol_version >= 10:
            write_u8(stream, info.status.mode)

        yield PacketType.BanchoUserPresence, stream.data
