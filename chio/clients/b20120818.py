
from typing import Iterable, Tuple
from .b20120806 import b20120806
from ..constants import *
from ..types import *
from ..io import *

class b20120818(b20120806):
    """
    b20120818 changes the "mods" datatype from s16 to u32.
    """
    version = 20120818
    protocol_version = 11

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        stream = MemoryStream()
        write_u8(stream, status.action)
        write_string(stream, status.text)
        write_string(stream, status.beatmap_checksum)

        if cls.protocol_version >= 11:
            write_u32(stream, status.mods)
        else:
            write_u16(stream, status.mods)

        write_u8(stream, status.mode)
        write_s32(stream, status.beatmap_id)
        return stream.data

    @classmethod
    def read_user_status(cls, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = Status(read_u8(stream))
        status.text = read_string(stream)
        status.beatmap_checksum = read_string(stream)

        if cls.protocol_version >= 11:
            status.mods = Mods(read_u32(stream))
        else:
            status.mods = Mods(read_u16(stream))

        status.mode = Mode(read_u8(stream))
        status.beatmap_id = read_s32(stream)
        return status

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u16(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)

        if cls.protocol_version >= 11:
            write_u32(stream, match.mods.value)
        else:
            write_u16(stream, match.mods.value)

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
        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u16(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))

        if cls.protocol_version >= 11:
            match.mods = Mods(read_u32(stream))
        else:
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

        for slot in match.slots:
            slot.team = SlotTeam(read_u8(stream))

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        match.host_id = read_s32(stream)
        match.mode = Mode(read_u8(stream))
        match.scoring_type = ScoringType(read_u8(stream))
        match.team_type = TeamType(read_u8(stream))
        return match
