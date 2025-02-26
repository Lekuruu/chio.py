
from typing import Iterable, Tuple
from .b20120518 import b20120518
from ..constants import *
from ..types import *
from ..io import *

class b20120703(b20120518):
    """
    b20120703 introduces a new packet to change match passwords.
    """
    version = 20120703

    @classmethod
    def read_match_change_password(cls, stream: MemoryStream) -> Match:
        return cls.read_match(stream)

    @classmethod
    def write_match_change_password(cls, password: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, password)
        yield PacketType.BanchoMatchChangePassword, stream.data
