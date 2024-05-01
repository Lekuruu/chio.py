
from enum import IntEnum

class Mode(IntEnum):
    Osu          = 0
    Taiko        = 1
    CatchTheBeat = 2
    OsuMania     = 3

    @classmethod
    def from_alias(cls, input: str):
        if input not in ('osu', 'taiko', 'fruits', 'mania'):
            return

        return {
            'osu': Mode.Osu,
            'taiko': Mode.Taiko,
            'fruits': Mode.CatchTheBeat,
            'mania': Mode.OsuMania
        }[input]

    @property
    def formatted(self) -> str:
        return {
            Mode.Osu: 'osu!',
            Mode.Taiko: 'Taiko',
            Mode.CatchTheBeat: 'CatchTheBeat',
            Mode.OsuMania: 'osu!mania'
        }[self]

    @property
    def alias(self) -> str:
        return {
            Mode.Osu: 'osu',
            Mode.Taiko: 'taiko',
            Mode.CatchTheBeat: 'fruits',
            Mode.OsuMania: 'mania'
        }[self]
