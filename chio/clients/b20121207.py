from .b20121203 import b20121203
from ..io import *

class b20121207(b20121203):
    """
    b20121207 allows tourney clients to request multiplayer match information.
    """
    version = 20121207

    @classmethod
    def read_tournament_match_info(cls, stream: MemoryStream) -> int:
        return read_s32(stream)
