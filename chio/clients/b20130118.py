
from typing import Iterable, Tuple
from .b20121225 import b20121225
from ..constants import *
from ..types import *
from ..io import *

class b20130118(b20121225):
    """
    b20130118 adds freemod support to multiplayer matches.
    """
    version = 20130118
    protocol_version = 16

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u16(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_u32(stream, match.mods.value)
        write_string(stream, match.name)
        write_string(stream, match.password)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)

        for slot in match.slots:
            write_u8(stream, slot.status.value)

        for slot in match.slots:
            write_u8(stream, slot.team)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        write_s32(stream, match.host_id)
        write_u8(stream, match.mode)
        write_u8(stream, match.scoring_type)
        write_u8(stream, match.team_type)

        if cls.protocol_version >= 16:
            write_boolean(stream, match.freemod)

        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u16(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.mods = Mods(read_u32(stream))
        match.name = read_string(stream)
        match.password = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)
        match.slots = [
            MatchSlot(status=SlotStatus(read_u8(stream)))
            for _ in range(cls.slot_size)
        ]

        for slot in match.slots:
            slot.team = SlotTeam(read_u8(stream))

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        match.host_id = read_s32(stream)
        match.mode = Mode(read_u8(stream))
        match.scoring_type = ScoringType(read_u8(stream))
        match.team_type = TeamType(read_u8(stream))

        if cls.protocol_version >= 16:
            match.freemod = read_boolean(stream)

        return match
