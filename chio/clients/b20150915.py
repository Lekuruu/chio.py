
from typing import Iterable, Tuple
from .b20150826 import b20150826
from ..constants import *
from ..types import *
from ..io import *

class b20150915(b20150826):
    """
    b20150915 drops support for 8-player multiplayer matches entirely.
    """
    version = 20150915
    slot_size = 16
    protocol_version = 19

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

        if match.freemod:
            for slot in match.slots:
                write_u32(stream, slot.mods)

        if cls.protocol_version >= 18:
            write_u32(stream, match.seed)

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

        if match.freemod:
            for slot in match.slots:
                slot.mods = Mods(read_u32(stream))

        if cls.protocol_version >= 18:
            match.seed = read_u32(stream)

        return match
