
from typing import Iterable, Tuple
from .b20140731 import b20140731
from ..constants import *
from ..types import *
from ..io import *

class b20141104(b20140731):
    """
    b20141104 allows the client to switch to a tournament server & abort a match.
    """
    version = 20141104

    @classmethod
    def write_switch_tournament_server(cls, server: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, server)
        yield PacketType.BanchoSwitchTournamentServer, stream.data

    @classmethod
    def write_match_abort(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchAbort, b''
