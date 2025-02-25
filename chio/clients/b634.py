
from typing import Iterable, Tuple
from .b613 import b613
from ..constants import *
from ..types import *
from ..io import *

class b634(b613):
    """
    b634 adds the monitor packet.
    """
    version = 634

    @classmethod
    def write_monitor(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMonitor, b''
