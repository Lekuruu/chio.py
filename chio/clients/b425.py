
from typing import Iterable, Tuple

from .b402 import b402
from ..constants import *
from ..io import *

class b425(b402):
    """
    b425 adds support for user permissions.
    """
    version = 425

    @classmethod
    def write_login_permissions(cls, permissions: Permissions) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, permissions.value)
        yield PacketType.BanchoLoginPermissions, stream.data
