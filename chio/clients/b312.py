
from typing import Tuple, Iterable
from .b298 import b298
from ..constants import *
from ..types import *
from ..io import *

class b312(b298):
    """
    b312 adds the match start & update packets, as well
    as the "InProgress" boolean inside the match struct.
    """
    version = 312

    @classmethod
    def write_match_start(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchStart, b""

    @classmethod
    def write_match_score_update(cls, frame: ScoreFrame) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        cls.write_score_frame(stream, frame)
        yield PacketType.BanchoMatchScoreUpdate, stream.data

    @classmethod
    def read_match_start(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_score_update(cls, stream: MemoryStream) -> ScoreFrame:
        return cls.read_score_frame(stream)
    
    @classmethod
    def read_match_complete(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        slots_open = [
            slot.status == SlotStatus.Open
            for slot in match.slots
        ]

        slots_used = [
            slot.has_player
            for slot in match.slots
        ]

        slots_ready = [
            slot.status == SlotStatus.Ready
            for slot in match.slots
        ]

        stream = MemoryStream()
        write_u8(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_string(stream, match.name)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)
        write_bool_list(stream, slots_open)
        write_bool_list(stream, slots_used)
        write_bool_list(stream, slots_ready)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u8(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.name = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)

        slots_open = read_bool_list(stream)
        slots_used = read_bool_list(stream)
        slots_ready = read_bool_list(stream)
        match.slots = []

        for i in range(cls.slot_size):
            slot = MatchSlot()
            slot.status = SlotStatus.Open if slots_open[i] else SlotStatus.Locked
            slot.status = SlotStatus.NotReady if slots_used[i] else slot.status
            slot.status = SlotStatus.Ready if slots_ready[i] else slot.status

            if slot.has_player:
                slot.user_id = read_s32(stream)

            match.slots.append(slot)

        return match
