
from chio.streams import StreamOut
from chio.objects import (
    bReplayFrameBundle,
    bBeatmapInfoReply,
    bStatusUpdate,
    bBeatmapInfo,
    bReplayFrame,
    bScoreFrame,
    bUserInfo,
    bUserQuit,
    bMessage,
    bChannel,
    bMatch
)

from typing import List, Optional

from .constants import ResponsePacket, Completeness
from ..writer import BaseWriter

class Writer(BaseWriter):
    def __init__(self) -> None:
        self.stream = StreamOut()

    def write_intlist(self, list: List[int]):
        self.stream.s32(len(list))
        [self.stream.s32(num) for num in list]

    def write_channel(self, channel: bChannel):
        self.stream.string(channel.name)

    def write_message(self, msg: bMessage):
        self.stream.string(msg.sender)
        self.stream.string(msg.content)
        self.stream.string(msg.target)

    def write_presence(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.u8(Completeness.Full.value)
        self.write_status(info.status)

        # Stats
        self.stream.s64(info.rscore)
        self.stream.float(info.accuracy)
        self.stream.s32(info.playcount)
        self.stream.s64(info.tscore)
        self.stream.s32(info.rank)

        # Presence
        self.stream.string(info.username)
        self.stream.string(f'{info.user_id}') # Avatar Filename
        self.stream.u8(info.timezone + 24)
        self.stream.string(info.city)
        self.stream.u8(info.permissions.value)
        self.stream.float(info.longitude)
        self.stream.float(info.latitude)

    def write_stats(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.u8(Completeness.Statistics.value)
        self.write_status(info.status)

        # Stats
        self.stream.s64(info.rscore)
        self.stream.float(info.accuracy)
        self.stream.s32(info.playcount)
        self.stream.s64(info.tscore)
        self.stream.s32(info.rank)

    def write_status(self, status: bStatusUpdate):
        self.stream.u8(status.action.value)
        self.stream.bool(True) # Beatmap Update
        self.stream.string(status.text)
        self.stream.string(status.beatmap_checksum)
        self.stream.u16(status.mods.value)
        self.stream.u8(status.mode.value)
        self.stream.s32(status.beatmap_id)

    def write_quit(self, state: bUserQuit):
        self.stream.s32(state.user_id)

    def write_beatmap_info(self, info: bBeatmapInfo):
        self.stream.s16(info.index)
        self.stream.s32(info.beatmap_id)
        self.stream.s32(info.beatmapset_id)
        self.stream.s32(info.thread_id)
        self.stream.u8(info.ranked)
        self.stream.u8(info.osu_rank.value)
        self.stream.u8(info.fruits_rank.value)
        self.stream.u8(info.taiko_rank.value)
        self.stream.string(info.checksum)

    def write_beatmap_info_reply(self, reply: bBeatmapInfoReply):
        self.stream.s32(len(reply.beatmaps))
        [self.write_beatmap_info(info) for info in reply.beatmaps]

    def write_replayframe(self, frame: bReplayFrame):
        self.stream.u8(frame.button_state.value)
        self.stream.u8(frame.legacy_byte)
        self.stream.float(frame.mouse_x)
        self.stream.float(frame.mouse_y)
        self.stream.s32(frame.time)

    def write_scoreframe(self, frame: bScoreFrame):
        self.stream.s32(frame.time)
        self.stream.u8(frame.id)
        self.stream.u16(frame.c300)
        self.stream.u16(frame.c100)
        self.stream.u16(frame.c50)
        self.stream.u16(frame.cGeki)
        self.stream.u16(frame.cKatu)
        self.stream.u16(frame.cMiss)
        self.stream.s32(frame.total_score)
        self.stream.u16(frame.max_combo)
        self.stream.u16(frame.current_combo)
        self.stream.bool(frame.perfect)
        self.stream.u8(frame.hp)
        self.stream.u8(frame.tag_byte)

    def write_replayframe_bundle(self, bundle: bReplayFrameBundle):
        self.stream.u16(len(bundle.frames))
        [self.write_replayframe(frame) for frame in bundle.frames]
        self.stream.u8(bundle.action.value)

        if bundle.score_frame:
            self.write_scoreframe(bundle.score_frame)

    def write_match(self, match: bMatch):
        self.stream.u8(match.id)

        self.stream.bool(match.in_progress)
        self.stream.u8(match.type.value)
        self.stream.u16(match.mods.value)

        self.stream.string(match.name)
        self.stream.string(match.password)
        self.stream.string(match.beatmap_text)
        self.stream.s32(match.beatmap_id)
        self.stream.string(match.beatmap_checksum)

        [self.stream.u8(slot.status.value) for slot in match.slots]
        [self.stream.u8(slot.team.value) for slot in match.slots]
        [self.stream.s32(slot.player_id) for slot in match.slots if slot.has_player]

        self.stream.s32(match.host_id)
        self.stream.u8(match.mode.value)
        self.stream.u8(match.scoring_type.value)
        self.stream.u8(match.team_type.value)
