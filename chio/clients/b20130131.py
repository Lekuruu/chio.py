
from typing import Iterable, Tuple
from .b20130118 import b20130118
from ..constants import *
from ..types import *
from ..io import *

class b20130131(b20130118):
    """
    b20130121 allows users to block private messages from non-friends.
    """
    version = 20130131

    @classmethod
    def write_user_dms_blocked(cls, username: str) -> Iterable[Tuple[PacketType, bytes]]:
        _, data = next(cls.write_message(Message("", "", username)))
        yield PacketType.BanchoUserDmsBlocked, data

    @classmethod
    def read_change_friend_only_dms(cls, stream: MemoryStream) -> bool:
        return read_s32(stream) == 1
