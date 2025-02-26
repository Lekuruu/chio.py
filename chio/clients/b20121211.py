
from typing import Iterable, Tuple
from .b20121207 import b20121207
from ..constants import *
from ..types import *
from ..io import *

class b20121211(b20121207):
    """
    b20121211 deprecates the lobby user list.
    """
    version = 20121211

    @classmethod
    def write_lobby_join(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        return []

    @classmethod
    def write_lobby_part(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        return []
