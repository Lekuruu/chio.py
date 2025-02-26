
from typing import Iterable, Tuple
from .b20140528 import b20140528
from ..constants import *
from ..types import *
from ..io import *

class b20140716(b20140528):
    """
    b20140716 sends the restriction status to the client.
    """
    version = 20140716

    @classmethod
    def write_account_restricted(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoAccountRestricted, b""
