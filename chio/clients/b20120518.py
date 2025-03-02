
from typing import Iterable, Tuple
from .b1820 import b1820
from ..constants import *
from ..types import *
from ..io import *

class b20120518(b1820):
    """
    b20120518 introduced the "ChannelInfoComplete" packet.
    """
    version = 20120518

    @classmethod
    def write_channel_info_complete(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoChannelInfoComplete, b""
