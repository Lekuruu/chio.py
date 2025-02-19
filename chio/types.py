
from .constants import RankedStatus, SlotStatus
from dataclasses import dataclass
from typing import List, Optional
from hashlib import md5

__all__ = [
    "UserInfo",
    "UserPresence",
    "UserStats",
    "UserStatus",
    "UserQuit",
    "Message",
    "Channel",
    "BeatmapInfo",
    "BeatmapInfoReply",
    "BeatmapInfoRequest",
    "ReplayFrame",
    "ScoreFrame",
    "ReplayFrameBundle",
    "MatchSlot",
    "Match",
    "MatchJoin",
    "TitleUpdate"
]

@dataclass
class UserPresence:
    is_irc: bool
    timezone: int
    country_index: int
    permissions: int
    longitude: float
    latitude: float
    city: str

@dataclass
class UserStats:
    rank: int
    rscore: int
    tscore: int
    accuracy: float
    playcount: int
    pp: int

@dataclass
class UserStatus:
    action: int
    text: str
    mods: int
    mode: int
    beatmap_checksum: str
    beatmap_id: int
    update_stats: bool

@dataclass
class UserInfo:
    id: int
    name: str
    presence: Optional[UserPresence]
    status: Optional[UserStatus]
    stats: Optional[UserStats]

    @property
    def avatar_filename(self) -> str:
        return f"{self.id}_000.png"

@dataclass
class UserQuit:
    info: Optional[UserInfo]
    quit_state: int

@dataclass
class Message:
    sender: str
    content: str
    target: str
    sender_id: int

@dataclass
class Channel:
    name: str
    topic: str
    owner: str
    user_count: int

@dataclass
class BeatmapInfo:
    index: int
    beatmap_id: int
    beatmap_set_id: int
    thread_id: int
    ranked_status: int
    osu_rank: int
    taiko_rank: int
    fruits_rank: int
    mania_rank: int
    checksum: str

    @property
    def is_ranked(self) -> bool:
        return self.ranked_status in (RankedStatus.Ranked, RankedStatus.Approved)

@dataclass
class BeatmapInfoReply:
    beatmaps: List[BeatmapInfo]

@dataclass
class BeatmapInfoRequest:
    filenames: List[str]
    ids: List[int]

@dataclass
class ReplayFrame:
    button_state: int
    legacy_byte: int
    mouse_x: float
    mouse_y: float
    time: int

@dataclass
class ScoreFrame:
    time: int
    id: int
    total_300: int
    total_100: int
    total_50: int
    total_geki: int
    total_katu: int
    total_miss: int
    total_score: int
    max_combo: int
    current_combo: int
    perfect: bool
    hp: int
    tag_byte: int

    @property
    def passed(self) -> bool:
        return False # TODO

    @property
    def checksum(self) -> str:
        data = (
            f"{self.time}{self.passed}{self.total_300}{self.total_50}{self.total_geki}"
            f"{self.total_katu}{self.total_miss}{self.current_combo}"
            f"{self.max_combo}{self.hp}"
        )
        return md5(data.encode()).hexdigest()

@dataclass
class ReplayFrameBundle:
    action: int
    extra: int
    frames: List[ReplayFrame]
    frame: Optional[ScoreFrame]

@dataclass
class MatchSlot:
    user_id: int
    status: int
    team: int
    mods: int

    @property
    def has_player(self) -> bool:
        return bool(SlotStatus.HasPlayer & self.status)

@dataclass
class Match:
    id: int
    in_progress: bool
    type: int
    mods: int
    name: str
    password: str
    beatmap_text: str
    beatmap_id: int
    beatmap_checksum: str
    slots: List[MatchSlot]
    host_id: int
    mode: int
    scoring_type: int
    team_type: int
    freemod: bool
    seed: int

@dataclass
class MatchJoin:
    match_id: int
    password: str

@dataclass
class TitleUpdate:
    image_url: str
    redirect_url: str
