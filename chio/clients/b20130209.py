
from typing import Iterable, Tuple

from .b20130131 import b20130131
from ..constants import *
from ..types import *

class b20130209(b20130131):
    """
    b20130209 adds the target silenced packet, which
    informs the client, that a user has been silenced.
    """
    version = 20130209

    @classmethod
    def write_target_is_silenced(cls, username: str) -> Iterable[Tuple[PacketType, bytes]]:
        _, data = next(cls.write_message(Message("", "", username)))
        yield PacketType.BanchoTargetIsSilenced, data
