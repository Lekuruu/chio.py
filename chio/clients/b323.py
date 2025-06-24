
from typing import Iterable, Tuple
from .b320 import b320
from ..constants import *
from ..types import *
from ..io import *

class b323(b320):
    """
    b323 changes the structure of user stats
    and adds the "MatchChangeBeatmap" packet
    """
    version = 323

    @classmethod
    def convert_input_packet(cls, packet: int) -> PacketType:
        if packet == 11:
            # "IrcJoin" packet
            return PacketType.BanchoIrcJoin
        
        if packet == 50:
            # "MatchChangeBeatmap" packet
            return PacketType.OsuMatchChangeBeatmap

        if 11 < packet <= 45:
            packet -= 1

        return PacketType(packet)

    @classmethod
    def convert_output_packet(cls, packet: PacketType) -> int:
        if packet is PacketType.BanchoIrcJoin:
            # "IrcJoin" packet
            return 11

        if packet is PacketType.OsuMatchChangeBeatmap:
            # "MatchChangeBeatmap" packet
            return 50

        if 11 <= packet < 45:
            return packet.value + 1

        return packet.value

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_stats = info.status.update_stats

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_boolean(stream, write_stats)

        if write_stats:
            write_string(stream, info.name)
            write_u64(stream, info.stats.rscore)
            write_f32(stream, info.stats.accuracy)
            write_u32(stream, info.stats.playcount)
            write_u64(stream, info.stats.tscore)
            write_u32(stream, info.stats.rank)
            write_string(stream, info.avatar_filename)
            write_u8(stream, info.presence.timezone+24)
            write_string(stream, info.presence.country_string)

        stream.write(cls.write_status_update(info.status))
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        # We assume that the client has not seen this user before, so
        # we send two packets: one for the user stats, and one for the "presence".
        info.status.update_stats = True
        yield next(cls.write_user_stats(info))

        info.status.update_stats = False
        yield next(cls.write_user_stats(info))

    @classmethod
    def read_match_change_beatmap(cls, stream: MemoryStream) -> Match:
        return cls.read_match(stream)
