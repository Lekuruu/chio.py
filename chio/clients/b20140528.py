
from typing import Iterable, Tuple
from .b20130604 import b20130604
from ..constants import *
from ..types import *
from ..io import *

class b20140528(b20130604):
    """
    b20140528 allows for 16-player multiplayer matches, if
    the protocol version is set to 19 or higher.
    """
    version = 20140528
    protocol_version = 18
    slot_size = 16

    @classmethod
    def read_match(cls, stream):
        cls.slot_size = 16 if cls.protocol_version >= 19 else 8
        return super().read_match(stream)

    @classmethod
    def write_match(cls, match):
        cls.slot_size = 16 if cls.protocol_version >= 19 else 8
        return super().write_match(match)
