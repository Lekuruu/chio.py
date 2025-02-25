
from typing import Iterable, Tuple
from .b487 import b487
from ..constants import *
from ..types import *
from ..io import *

class b489(b487):
    """
    b489 adds support for game modes inside user status updates.
    """
    version = 489
    protocol_version = 1

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        stream = MemoryStream()
        write_u8(stream, status.action)

        beatmap_update = True
        write_boolean(stream, beatmap_update)

        if beatmap_update:
            write_string(stream, status.text)
            write_string(stream, status.beatmap_checksum)
            write_u16(stream, status.mods)

            if cls.protocol_version >= 1:
                write_u8(stream, status.mode)

        return stream.data

    @classmethod
    def read_user_status(cls, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = Status(read_u8(stream))
        beatmap_update = read_boolean(stream)

        if beatmap_update:
            status.text = read_string(stream)
            status.beatmap_checksum = read_string(stream)
            status.mods = Mods(read_u16(stream))

            if cls.protocol_version >= 1:
                status.mode = Mode(read_u8(stream))

        return status
