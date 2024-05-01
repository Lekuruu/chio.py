
from chio.objects import bUserInfo

from ..b1700.writer import Writer as BaseWriter
from ..b1700.constants import Completeness

class Writer(BaseWriter):
    def write_presence(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.u8(Completeness.Full.value)
        self.write_status(info.status)

        # Stats
        self.stream.s64(info.rscore)
        self.stream.float(info.accuracy)
        self.stream.s32(info.playcount)
        self.stream.s64(info.tscore)
        self.stream.s32(info.rank)

        # Presence
        self.stream.string(info.username)
        self.stream.string(f'{info.user_id}') # Avatar Filename
        self.stream.u8(info.timezone + 24)
        self.stream.string(info.city)
        self.stream.u8(info.permissions.value)
