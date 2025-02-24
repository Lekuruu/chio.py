
from typing import Iterable, Tuple
from .b591 import b591
from ..constants import *
from ..types import *
from ..io import *

class b613(b591):
    """
    b613 allows the client to leave channels.
    """
    version = 613

    @classmethod
    def read_channel_leave(cls, stream: MemoryStream) -> str:
        return read_string(stream)
