
from ..b399 import Writer as BaseWriter

from chio.constants import ClientStatus
from chio.objects import (
    bStatusUpdate,
    bUserInfo,
    bUserQuit
)

class Writer(BaseWriter):
    def write_presence(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.bool(True) # "newstats"
        self.stream.string(info.username)

        # Stats
        self.stream.s64(info.rscore)
        self.stream.float(info.accuracy)
        self.stream.s32(info.playcount)
        self.stream.s64(info.tscore)
        self.stream.s32(info.rank)

        # Presence
        self.stream.string(f'{info.user_id}_000.png') # Avatar Filename
        self.stream.u8(info.timezone + 24)
        self.stream.string(info.city)

        self.write_status(info.status, update=True)

    def write_stats(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.bool(False) # "newstats"

        self.write_status(info.status)

    def write_status(self, status: bStatusUpdate, update: bool = False):
        if update:
            # Set to "StatusUpdate"
            status.action = ClientStatus.Paused

        elif status.action > 9:
            # Workaround because of different enum values
            status.action = ClientStatus(status.action - 1)

        self.stream.u8(status.action.value)
        self.stream.string(status.text)
        self.stream.string(status.beatmap_checksum)
        self.stream.u16(status.mods.value)

    def write_quit(self, state: bUserQuit):
        self.stream.s32(state.user_id)
        self.stream.bool(False)
        self.write_status(state.info.status)
