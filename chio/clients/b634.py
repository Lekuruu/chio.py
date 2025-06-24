
from typing import Iterable, Tuple

from .b613 import b613
from ..constants import *
from ..io import *

class b634(b613):
    """
    b634 adds the monitor & player update request packets.
    """
    version = 634

    @classmethod
    def write_monitor(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMonitor, b''

    @classmethod
    def read_receive_updates(cls, stream: MemoryStream) -> PresenceFilter:
        return PresenceFilter(read_s32(stream))
