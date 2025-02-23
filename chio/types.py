
from .constants import *
from dataclasses import dataclass, field
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
    action: Status = Status.Idle
    text: str = ""
    mods: Mods = Mods.NoMod
    mode: Mode = Mode.Osu
    beatmap_checksum: str = ""
    beatmap_id: int = -1
    update_stats: bool = False

    def reset(self) -> None:
        self.action = Status.Idle
        self.text = ""
        self.mods = Mods.NoMod
        self.mode = Mode.Osu
        self.beatmap_checksum = ""
        self.beatmap_id = -1
        self.update_stats = False

@dataclass
class UserInfo:
    id: int
    name: str
    presence: UserPresence
    status: UserStatus
    stats: UserStats

    @property
    def avatar_filename(self) -> str:
        return f"{self.id}_000.png"

@dataclass
class UserQuit:
    info: UserInfo
    quit_state: int

@dataclass
class Message:
    sender: str
    content: str
    target: str
    sender_id: int = -1

    @property
    def is_direct_message(self) -> bool:
        return not self.target.startswith("#")

@dataclass
class Channel:
    name: str
    topic: str
    owner: str
    user_count: int = 0

@dataclass
class BeatmapInfo:
    index: int
    beatmap_id: int
    beatmapset_id: int
    thread_id: int
    ranked_status: RankedStatus
    osu_rank: Rank
    taiko_rank: Rank
    fruits_rank: Rank
    mania_rank: Rank
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
    button_state: ButtonState = ButtonState.NoButton
    legacy_byte: int = 0
    mouse_x: float = 0.0
    mouse_y: float = 0.0
    time: int = 0

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
    action: ReplayAction = ReplayAction.Standard
    frames: List[ReplayFrame] = field(default_factory=list)
    frame: Optional[ScoreFrame] = None
    extra: int = -1

@dataclass
class MatchSlot:
    user_id: int = -1
    status: SlotStatus = SlotStatus.Open
    team: SlotTeam = SlotTeam.Neutral
    mods: Mods = Mods.NoMod

    @property
    def has_player(self) -> bool:
        return bool(SlotStatus.HasPlayer & self.status)
    
    def reset(self) -> None:
        self.user_id = -1
        self.status = SlotStatus.Open
        self.team = SlotTeam.Neutral
        self.mods = Mods.NoMod

@dataclass
class Match:
    id: int = 0
    in_progress: bool = False
    type: MatchType = MatchType.Standard
    mods: Mods = Mods.NoMod
    name: str = ""
    password: str = ""
    beatmap_text: str = ""
    beatmap_id: int = -1
    beatmap_checksum: str = ""
    slots: List[MatchSlot] = field(default_factory=list)
    host_id: int = -1
    mode: Mode = Mode.Osu
    scoring_type: ScoringType = ScoringType.Score
    team_type: TeamType = TeamType.HeadToHead
    freemod: bool = False
    seed: int = 0

@dataclass
class MatchJoin:
    match_id: int = -1
    password: str = ""

@dataclass
class TitleUpdate:
    image_url: str = ""
    redirect_url: str = ""
