
from typing import Iterable, Tuple
from .b1800 import b1800
from ..constants import *
from ..types import *
from ..io import *

class b1817(b1800):
    """
    b1817 adds the ability to send multiplayer match invites to other users.
    """
    version = 1817

    @classmethod
    def write_invite(cls, invite_message: Message) -> Iterable[Tuple[PacketType, bytes]]:
        _, data = next(cls.write_message(invite_message))
        yield PacketType.BanchoInvite, data

    @classmethod
    def read_invite(cls, stream: MemoryStream) -> int:
        return read_s32(stream)
