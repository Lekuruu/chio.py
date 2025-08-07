
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
    is_irc: bool = False
    timezone: int = 0
    country_index: int = 0
    permissions: Permissions = Permissions.Regular
    longitude: float = 0.0
    latitude: float = 0.0
    city: str = ""

    @property
    def country_name(self) -> str:
        return CountryNames[self.country_index]

    @property
    def country_acronym(self) -> str:
        return CountryAcronyms[self.country_index]

    @property
    def country_string(self) -> str:
        return (
            self.country_name if not self.city else
            f"{self.country_name} / {self.city}"
        )

@dataclass
class UserStats:
    rank: int = 0
    rscore: int = 0
    tscore: int = 0
    accuracy: float = 0.0
    playcount: int = 0
    pp: int = 0

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
    id: int = 0
    name: str = ""
    presence: UserPresence = field(default_factory=UserPresence)
    status: UserStatus = field(default_factory=UserStatus)
    stats: UserStats = field(default_factory=UserStats)

    @property
    def avatar_filename(self) -> str:
        return f"{self.id}_000.png"

@dataclass
class UserQuit:
    info: UserInfo = field(default_factory=UserInfo)
    state: QuitState = QuitState.Gone

@dataclass
class Message:
    sender: str
    content: str
    target: str
    sender_id: int = -1

    @property
    def content_formatted(self) -> str:
        return ChatLinkModern.sub(r"(\2)[\1]", self.content)

    @property
    def is_direct_message(self) -> bool:
        return not self.target.startswith("#")

@dataclass
class Channel:
    name: str
    topic: str = ""
    owner: str = "BanchoBot"
    user_count: int = 0

@dataclass
class BeatmapInfo:
    index: int
    beatmap_id: int
    beatmapset_id: int
    thread_id: int
    ranked_status: RankedStatus
    checksum: str
    osu_rank: Rank = Rank.N
    taiko_rank: Rank = Rank.N
    fruits_rank: Rank = Rank.N
    mania_rank: Rank = Rank.N

    @property
    def is_ranked(self) -> bool:
        return self.ranked_status in (RankedStatus.Ranked, RankedStatus.Approved)

@dataclass
class BeatmapInfoReply:
    beatmaps: List[BeatmapInfo] = field(default_factory=list)

@dataclass
class BeatmapInfoRequest:
    filenames: List[str] = field(default_factory=list)
    ids: List[int] = field(default_factory=list)

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
    using_scorev2: bool = False
    combo_portion: float = 0.0
    bonus_portion: float = 0.0

    @property
    def passed(self) -> bool:
        return self.hp != 254

    @property
    def checksum(self) -> str:
        data = (
            f"{self.time}{self.passed}{self.total_300}{self.total_50}{self.total_geki}"
            f"{self.total_katu}{self.total_miss}{self.current_combo}"
            f"{self.max_combo}{self.hp}"
        )
        return md5(data.encode()).hexdigest()

    def total_hits(self, mode: Mode) -> int:
        if mode == Mode.CatchTheBeat:
            return self.total_50 + self.total_100 + self.total_300 + self.total_miss + self.total_katu

        elif mode == Mode.OsuMania:
            return self.total_300 + self.total_100 + self.total_50 + self.total_geki + self.total_katu + self.total_miss

        return self.total_50 + self.total_100 + self.total_300 + self.total_miss

    def accuracy(self, mode: Mode) -> float:
        if self.total_hits(mode) == 0:
            return 0.0

        if mode == Mode.Osu:
            return (
                ((self.total_300 * 300.0) + (self.total_100 * 100.0) + (self.total_50 * 50.0))
                / (self.total_hits(mode) * 300.0)
            )

        elif mode == Mode.Taiko:
            return ((self.total_100 * 0.5) + self.total_300) / self.total_hits(mode)

        elif mode == Mode.CatchTheBeat:
            return (self.total_300 + self.total_100 + self.total_50) / self.total_hits(mode)

        elif mode == Mode.OsuMania:
            return  (
                (
                    (self.total_50 * 50.0) + (self.total_100 * 100.0) +
                    (self.total_katu * 200.0) + ((self.total_300 + self.total_geki) * 300.0)
                )
                / (self.total_hits(mode) * 300.0)
            )

        else:
            return 0.0

    def rank(self, mode: Mode, mods: Mods) -> Rank:
        r300 = self.total_300 / self.total_hits(mode)
        r50 = self.total_50 / self.total_hits(mode)

        if r300 == 1:
            return (
                Rank.XH
                if Mods.Hidden in mods
                or Mods.Flashlight in mods
                else Rank.X
            )

        if r300 > 0.9 and r50 <= 0.01 and self.total_miss == 0:
            return (
                Rank.SH
                if Mods.Hidden in mods
                or Mods.Flashlight in mods
                else Rank.S
            )

        if (r300 > 0.8 and self.total_miss == 0) or (r300 > 0.9):
            return Rank.A

        if (r300 > 0.7 and self.total_miss == 0) or (r300 > 0.8):
            return Rank.B

        if (r300 > 0.6):
            return Rank.C

        return Rank.D

@dataclass
class ReplayFrameBundle:
    action: ReplayAction = ReplayAction.Standard
    frames: List[ReplayFrame] = field(default_factory=list)
    frame: Optional[ScoreFrame] = None
    extra: int = -1
    sequence: Optional[int] = None

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
