
from enum import IntEnum

class GameMode(IntEnum):
    Osu          = 0
    Taiko        = 1
    CatchTheBeat = 2
    OsuMania     = 3

    @classmethod
    def from_alias(cls, input: str):
        if input not in ('osu', 'taiko', 'fruits', 'mania'):
            return

        return {
            'osu': GameMode.Osu,
            'taiko': GameMode.Taiko,
            'fruits': GameMode.CatchTheBeat,
            'mania': GameMode.OsuMania
        }[input]

    @property
    def formatted(self) -> str:
        return {
            GameMode.Osu: 'osu!',
            GameMode.Taiko: 'Taiko',
            GameMode.CatchTheBeat: 'CatchTheBeat',
            GameMode.OsuMania: 'osu!mania'
        }[self]

    @property
    def alias(self) -> str:
        return {
            GameMode.Osu: 'osu',
            GameMode.Taiko: 'taiko',
            GameMode.CatchTheBeat: 'fruits',
            GameMode.OsuMania: 'mania'
        }[self]
