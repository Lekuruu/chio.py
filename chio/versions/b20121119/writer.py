
from chio.constants import AvatarExtension
from chio.objects import bUserInfo

from ..b20130329 import Writer as BaseWriter

class Writer(BaseWriter):
    def write_presence(self, info: bUserInfo):
        self.stream.s32(info.user_id)
        self.stream.string(info.username)
        self.stream.u8(AvatarExtension.PNG.value) # NOTE: Client will not send avatar request when NONE
        self.stream.u8(info.timezone + 24)
        self.stream.u8(info.country_index)
        self.stream.string(info.city)
        self.stream.u8(info.permissions.value)
        self.stream.float(info.longitude)
        self.stream.float(info.latitude)
        self.stream.s32(info.rank)
        self.stream.u8(info.mode.value)
