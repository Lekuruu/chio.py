
from typing import Iterable, Tuple
from .b1788 import b1788
from ..constants import *
from ..types import *
from ..io import *

class b1796(b1788):
    """
    b1796 changes the way how countries are sent to the client, and increases
    the total amount of match-slots that can be sent (u8 -> u16).
    """
    version = 1796

    @classmethod
    def write_match_update(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchUpdate, cls.write_match(match)

    @classmethod
    def write_match_new(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchNew, cls.write_match(match)

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
        yield PacketType.BanchoUserPresence, stream.data

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u16(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_u16(stream, match.mods.value)
        write_string(stream, match.name)
        write_string(stream, match.password)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)

        for slot in match.slots:
            write_u8(stream, slot.status.value)

        if cls.protocol_version >= 4:
            for slot in match.slots:
                write_u8(stream, slot.team)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        write_s32(stream, match.host_id)
        write_u8(stream, match.mode)

        if cls.protocol_version >= 3:
            write_u8(stream, match.scoring_type)
            write_u8(stream, match.team_type)

        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u16(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.mods = Mods(read_u16(stream))
        match.name = read_string(stream)
        match.password = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)
        match.slots = [
            MatchSlot(status=SlotStatus(read_u8(stream)))
            for _ in range(cls.slot_size)
        ]

        if cls.protocol_version >= 4:
            for slot in match.slots:
                slot.team = SlotTeam(read_u8(stream))

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        match.host_id = read_s32(stream)
        match.mode = Mode(read_u8(stream))

        if cls.protocol_version < 3:
            return match

        match.scoring_type = ScoringType(read_u8(stream))
        match.team_type = TeamType(read_u8(stream))
        return match
