
from dataclasses import dataclass
from typing import Optional

from ..constants import (
    ClientStatus,
    Permissions,
    QuitState,
    GameMode,
    Mods
)

@dataclass
class StatusUpdate:
    action: ClientStatus
    text: str = ""
    mods: Mods = Mods.NoMod
    mode: GameMode = GameMode.Osu
    beatmap_checksum: str = ""
    beatmap_id: int = -1

@dataclass
class UserPresence:
    user_id: int
    is_irc: bool
    username: str
    timezone: int
    country_code: int
    permissions: Permissions
    mode: GameMode
    longitude: float
    latitude: float
    rank: int
    city: Optional[str] = None

@dataclass
class UserStats:
    user_id: int
    status: StatusUpdate
    rscore: int
    tscore: int
    accuracy: float
    playcount: int
    rank: int
    pp: int

@dataclass
class UserQuit:
    user_id: int
    presence: UserPresence
    stats: UserStats
    quit_state: QuitState
