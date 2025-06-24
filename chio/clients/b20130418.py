
from typing import Iterable, Tuple
from .b20130303 import b20130303
from ..constants import *
from ..types import *
from ..io import *

class b20130418(b20130303):
    """
    b20130418 implements the mania random mod, which requires the "seed" field to be sent.
    """
    version = 20130418
    protocol_version = 18

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

    @classmethod
    def write_spectate_frames(cls, bundle: ReplayFrameBundle) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if cls.protocol_version >= 18:
            write_s32(stream, bundle.extra)

        write_u16(stream, len(bundle.frames))

        for frame in bundle.frames:
            stream.write(cls.write_replay_frame(frame))

        write_u8(stream, bundle.action)

        if bundle.frame:
            cls.write_score_frame(stream, bundle.frame)

        yield PacketType.BanchoSpectateFrames, stream.data

    @classmethod
    def read_spectate_frames(cls, stream: MemoryStream) -> ReplayFrameBundle:
        extra = -1

        if cls.protocol_version >= 18:
            extra = read_u32(stream)

        frames = [
            cls.read_replay_frame(stream)
            for _ in range(read_u16(stream))
        ]
        action = ReplayAction(read_u8(stream))
        frame = None

        if stream.available() > 0:
            frame = cls.read_score_frame(stream)

        return ReplayFrameBundle(action, frames, frame, extra)
