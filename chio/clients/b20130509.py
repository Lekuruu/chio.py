
from typing import Iterable, Tuple
from .b20130418 import b20130418
from ..constants import *
from ..types import *
from ..io import *

class b20130509(b20130418):
    """
    b20130509 reworks the updating system, and can now differentiate
    between forced updates and regular updates.
    """
    version = 20130509

    @classmethod
    def write_version_update_forced(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoVersionUpdateForced, b""
