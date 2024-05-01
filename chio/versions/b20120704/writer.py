
from ..b20120725 import Writer as BaseWriter

from chio.objects import bUserInfo

class Writer(BaseWriter):
    def write_stats(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.write_status(info.status)
        self.stream.u64(info.rscore)
        self.stream.float(info.accuracy)
        self.stream.s32(info.playcount)
        self.stream.u64(info.tscore)
        self.stream.s32(info.rank)
