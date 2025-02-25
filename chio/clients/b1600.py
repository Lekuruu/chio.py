
from typing import Iterable, Tuple
from .b1365 import b1365
from ..constants import *
from ..types import *
from ..io import *

class b1600(b1365):
    """
    b1600 adds /away commands.
    """
    version = 1600

    @classmethod
    def read_set_irc_away_message(cls, stream: MemoryStream) -> Message:
        return cls.read_message(stream)
