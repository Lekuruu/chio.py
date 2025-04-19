
from typing import Iterable, Tuple
from .b20121028 import b20121028
from ..constants import *
from ..types import *
from ..io import *

class b20121203(b20121028):
    """
    b20121203 optimizes the way how the user presence is sent to the client.
    """
    version = 20121203
    protocol_version = 13

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, cls.convert_user_id(info))
        write_string(stream, info.name)
        write_u8(stream, info.presence.timezone+24)
        write_u8(stream, info.presence.country_index)
        write_u8(stream, info.presence.permissions | info.status.mode << 5)
        write_f32(stream, info.presence.longitude)
        write_f32(stream, info.presence.latitude)
        write_s32(stream, info.stats.rank)
        write_u8(stream, info.status.mode)
        yield PacketType.BanchoUserPresence, stream.data
