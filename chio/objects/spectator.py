
from dataclasses import dataclass
from typing import List, Optional

from ..constants import (
    ReplayAction,
    ButtonState,
    GameMode,
    Grade,
    Mods
)

import hashlib

@dataclass
class ScoreFrame:
    time: int
    id: int
    c300: int
    c100: int
    c50: int
    cGeki: int
    cKatu: int
    cMiss: int
    total_score: int
    max_combo: int
    current_combo: int
    perfect: bool
    hp: int
    tag_byte: int = 0

    @property
    def checksum(self) -> str:
        """Checksum calculation used in version b323"""
        return hashlib.md5(''.join([
            str(self.time),
            'false', # "pass" ?
            str(self.c300),
            str(self.c50),
            str(self.cGeki),
            str(self.cKatu),
            str(self.cMiss),
            str(self.current_combo),
            str(self.max_combo),
            str(self.hp),
        ]).encode()).hexdigest()

@dataclass
class ReplayFrame:
    button_state: ButtonState
    legacy_byte: int
    mouse_x: float
    mouse_y: float
    time: int

    # NOTE: The legacy_byte was originally used to store if the left key
    #       was pressed. This is no longer the case. You can see the
    #       implementation in b338.

@dataclass
class ReplayFrameBundle:
    extra: int
    action: ReplayAction
    frames: List[ReplayFrame]
    score_frame: Optional[ScoreFrame] = None
