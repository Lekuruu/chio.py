
from typing import Iterable, Tuple
from .b425 import b425
from ..constants import *
from ..types import *
from ..io import *

class b452(b425):
    """
    b452 adds friend management & user permissions to the user's stats.
    """
    version = 452

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
        write_string(stream, info.presence.city)
        write_u8(stream, info.presence.permissions)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_friends_list(cls, friends: Iterable[int]) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_list_s32(stream, list(friends))
        yield PacketType.BanchoFriendsList, stream.data

    @classmethod
    def read_friends_add(cls, stream: Stream) -> int:
        return read_s32(stream)

    @classmethod
    def read_friends_remove(cls, stream: Stream) -> int:
        return read_s32(stream)
