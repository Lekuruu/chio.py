
from dataclasses import dataclass
from typing import Optional

from ..constants import (
    ClientStatus,
    Permissions,
    QuitState,
    Mode,
    Mods
)

@dataclass
class StatusUpdate:
    action: ClientStatus
    text: str = ""
    mods: Mods = Mods.NoMod
    mode: Mode = Mode.Osu
    beatmap_checksum: str = ""
    beatmap_id: int = -1

@dataclass
class UserInfo:
    user_id: int
    is_irc: bool
    username: str
    country_index: int # Index of a country in "chio.objects.Countries"
    timezone: int
    permissions: Permissions
    mode: Mode
    longitude: float
    latitude: float
    status: StatusUpdate
    rscore: int
    tscore: int
    accuracy: float
    playcount: int
    rank: int
    pp: int
    city: Optional[str] = None
    stats_update: bool = False # Required for b319 and lower

@dataclass
class UserQuit:
    user_id: int
    info: UserInfo
    quit_state: QuitState
