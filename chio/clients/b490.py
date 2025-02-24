
from typing import Iterable, Tuple
from .b489 import b489
from ..constants import *
from ..types import *
from ..io import *

class b490(b489):
    """
    b490 now sends the beatmap ID in user status updates.
    """
    version = 490

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        action = status.action if not status.update_stats else Status.StatsUpdate
        stream = MemoryStream()
        write_u8(stream, action)

        beatmap_update = True
        write_boolean(stream, beatmap_update)

        if beatmap_update:
            write_string(stream, status.text)
            write_string(stream, status.beatmap_checksum)
            write_u16(stream, status.mods)
            write_u8(stream, status.mode)
            write_s32(stream, status.beatmap_id)

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
            status.mode = Mode(read_u8(stream))
            status.beatmap_id = read_s32(stream)

        return status
