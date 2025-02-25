
from typing import Iterable, Tuple
from .b1600 import b1600
from ..constants import *
from ..types import *
from ..io import *

class b1788(b1600):
    """
    b1788 includes probably the largest amount of changes to the bancho protocol overall.
    - bUserStats split up into Presence & Stats
    - Server no longer needs to send bUserStats to clients, instead the client requests it themselves
    - The `count` datatype for bListInt got changed into a signed 16-bit integer
    - The user status no longer contains a boolean for updates
    - IrcJoin packet is now deprecated, in favor of user IDs being negative if they are IRC users
    - The restart packet got introduced, which informs the client that bancho is restarting
    """
    version = 1788
    requires_status_updates = False

    @classmethod
    def convert_input_packet(cls, packet: int) -> PacketType:
        return PacketType(packet)

    @classmethod
    def convert_output_packet(cls, packet: PacketType) -> int:
        return packet.value

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        # User IDs are now negative if they are IRC users
        user_id = (
            abs(info.id) if not info.presence.is_irc else
            -abs(info.id)
        )

        write_u32(stream, user_id)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        # User IDs are now negative if they are IRC users
        user_id = (
            abs(info.id) if not info.presence.is_irc else
            -abs(info.id)
        )

        write_u32(stream, user_id)
        write_string(stream, info.name)
        write_u8(stream, AvatarExtension.Empty)
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.city)
        write_u8(stream, info.presence.permissions)
        write_f32(stream, info.presence.longitude)
        write_f32(stream, info.presence.latitude)
        yield PacketType.BanchoUserPresence, stream.data

    @classmethod
    def read_user_status(cls, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = Status(read_u8(stream))
        status.text = read_string(stream)
        status.beatmap_checksum = read_string(stream)
        status.mods = Mods(read_u16(stream))
        status.mode = Mode(read_u8(stream))
        status.beatmap_id = read_s32(stream)
        return status

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        stream = MemoryStream()
        write_u8(stream, status.action)
        write_string(stream, status.text)
        write_string(stream, status.beatmap_checksum)
        write_u16(stream, status.mods)
        write_u8(stream, status.mode)
        write_s32(stream, status.beatmap_id)
        return stream.data

    @classmethod
    def write_friends_list(cls, friends: Iterable[int]) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_list_s16(stream, list(friends))
        yield PacketType.BanchoFriendsList, stream.data

    @classmethod
    def read_user_stats_request(cls, stream: MemoryStream) -> Iterable[int]:
        return read_list_s16(stream)
    
    @classmethod
    def write_restart(cls, retry_after_ms: int = 5000) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, retry_after_ms)
        yield PacketType.BanchoRestart, stream.data

    @classmethod
    def write_irc_join(cls, name: str) -> Iterable[Tuple[PacketType, bytes]]:
        return []
