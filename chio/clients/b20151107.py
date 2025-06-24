from .b20151106 import b20151106
from ..io import *

class b20151107(b20151106):
    """
    b20151107 adds tournament client chat support.
    """
    version = 20151107

    @classmethod
    def read_tournament_join_match_channel(cls, stream: MemoryStream) -> int:
        return read_s32(stream)

    @classmethod
    def read_tournament_leave_match_channel(cls, stream: MemoryStream) -> int:
        return read_s32(stream)
