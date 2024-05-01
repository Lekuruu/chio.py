
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

from typing import Optional, List
from enum import Enum
from abc import ABC

class BaseWriter(ABC):
    def __init__(self) -> None:
        self.stream = StreamOut()

    def write_intlist(self, list: List[int]):
        ...

    def write_channel(self, channel: bChannel):
        ...

    def write_message(self, msg: bMessage):
        ...

    def write_presence(self, presence: bUserInfo):
        ...

    def write_stats(self, info: bUserInfo):
        ...

    def write_quit(self, state: bUserQuit):
        ...

    def write_status(self, status: bStatusUpdate):
        ...

    def write_beatmap_info(self, info: bBeatmapInfo):
        ...

    def write_beatmap_info_reply(self, reply: bBeatmapInfoReply):
        ...

    def write_match(self, match: bMatch):
        ...

    def write_replayframe(self, frame: bReplayFrame):
        ...

    def write_scoreframe(self, frame: bScoreFrame):
        ...

    def write_replayframe_bundle(self, bundle: bReplayFrameBundle):
        ...
