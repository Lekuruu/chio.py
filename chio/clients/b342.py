
from typing import Iterable, Tuple
from .b340 import b340
from ..constants import *
from ..types import *
from ..io import *

class b342(b340):
    """
    b342 adds the multiplayer skip packets.
    """
    version = 342

    @classmethod
    def write_match_skip(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchSkip, b''

    @classmethod
    def read_match_skip_request(cls, stream: MemoryStream) -> None:
        pass
