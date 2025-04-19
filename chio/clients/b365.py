
from copy import copy
from typing import Iterable, Tuple
from .b354 import b354
from ..constants import *
from ..types import *
from ..io import *

class b365(b354):
    """
    b365 adds a level display on the user panel, which has a bug that causes
    the client to crash, when the user has a very high total score.
    """
    version = 365

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        total_score = copy(info.stats.tscore)

        # Cap total score & write stats
        info.stats.tscore = min(info.stats.tscore, 17705429348)
        yield next(super().write_user_stats(info))

        # Re-apply original value
        info.stats.tscore = total_score
    
    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        total_score = copy(info.stats.tscore)

        # Cap total score & write presence
        info.stats.tscore = min(info.stats.tscore, 17705429348)
        yield next(super().write_user_presence(info))

        # Re-apply original value
        info.stats.tscore = total_score
