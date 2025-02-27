
from typing import Iterable, Tuple
from .b504 import b504
from ..constants import *
from ..types import *
from ..io import *

class b535(b504):
    """
    b535 adds the scoring & team types for multiplayer matches, as well
    as the tag multiplayer game mode.
    """
    version = 535
    protocol_version = 3

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u8(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_u16(stream, match.mods.value)
        write_string(stream, match.name)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)

        for slot in match.slots:
            write_u8(stream, slot.status.value)

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
        match.id = read_u8(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.mods = Mods(read_u16(stream))
        match.name = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)
        match.slots = [
            MatchSlot(status=SlotStatus(read_u8(stream)))
            for _ in range(cls.slot_size)
        ]

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        match.host_id = read_s32(stream)
        match.mode = Mode(read_u8(stream))

        if cls.protocol_version < 3:
            return match

        # There are multiple versions of b535, which have different
        # levels of implementation for the new match data, so we need
        # to check if the data is available before reading it.

        if stream.available() > 0:
            match.scoring_type = ScoringType(read_u8(stream))

        if stream.available() > 0:
            match.team_type = TeamType(read_u8(stream))

        return match

    @classmethod
    def write_score_frame(cls, stream: MemoryStream, frame: ScoreFrame) -> None:
        write_s32(stream, frame.time)
        write_u8(stream, frame.id)
        write_u16(stream, frame.total_300)
        write_u16(stream, frame.total_100)
        write_u16(stream, frame.total_50)
        write_u16(stream, frame.total_geki)
        write_u16(stream, frame.total_katu)
        write_u16(stream, frame.total_miss)
        write_u32(stream, frame.total_score)
        write_u16(stream, frame.max_combo)
        write_u16(stream, frame.current_combo)
        write_boolean(stream, frame.perfect)
        write_u8(stream, frame.hp)
        write_u8(stream, frame.tag_byte)

    @classmethod
    def read_score_frame(cls, stream: MemoryStream) -> ScoreFrame:
        frame = ScoreFrame(
            time=read_s32(stream),
            id=read_u8(stream),
            total_300=read_u16(stream),
            total_100=read_u16(stream),
            total_50=read_u16(stream),
            total_geki=read_u16(stream),
            total_katu=read_u16(stream),
            total_miss=read_u16(stream),
            total_score=read_u32(stream),
            max_combo=read_u16(stream),
            current_combo=read_u16(stream),
            perfect=read_boolean(stream),
            hp=read_u8(stream),
            tag_byte=0
        )

        if stream.available() > 0:
            # Similar to the scoring type in the match data; the
            # client has a new implementation for the tag byte
            frame.tag_byte = read_u8(stream)

        return frame
    
    @classmethod
    def write_title_update(cls, update: TitleUpdate) -> Iterable[Tuple[PacketType, bytes]]:
        # This is currently only used to refresh the title image, without sending the link
        # over the packet, i.e. it's still using `/web/osu-title-image.php` under the hood.
        yield PacketType.BanchoTitleUpdate, b""
