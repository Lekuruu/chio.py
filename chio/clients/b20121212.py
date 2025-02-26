
from typing import Iterable, Tuple
from .b20121211 import b20121211
from ..constants import *
from ..types import *
from ..io import *

class b20121212(b20121211):
    """
    b20121212 adds support for the user silenced packet.
    """
    version = 20121212

    @classmethod
    def write_user_silenced(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoUserSilenced, stream.data
