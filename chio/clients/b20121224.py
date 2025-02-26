
from typing import Iterable, Tuple
from .b20121212 import b20121212
from ..constants import *
from ..types import *
from ..io import *

class b20121224(b20121212):
    """
    b20121224 deprecates the irc quit packet, in favor of a unified quit packet.
    """
    version = 20121224

    @classmethod
    def write_user_quit(cls, quit: UserQuit) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, quit.user_id)
        write_u8(stream, quit.state)
        yield PacketType.BanchoUserQuit, stream.data
