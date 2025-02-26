
from typing import Iterable, Tuple
from .b20130509 import b20130509
from ..constants import *
from ..types import *
from ..io import *

class b20130604(b20130509):
    """
    b20130604 allows for forced bancho server switching, after
    the client was idle for a certain amount of time.
    """
    version = 20130604

    @classmethod
    def write_switch_server(cls, after_idle_time: int = 3600) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(after_idle_time)
        yield PacketType.BanchoSwitchServer, stream.data
