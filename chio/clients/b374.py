
from typing import Iterable, Tuple
from .b365 import b365
from ..constants import *
from ..types import *
from ..io import *

class b374(b365):
    """
    b374 adds the ButtonState constant, which deprectaes
    the old button left/right booleans.
    """
    version = 374

    @classmethod
    def write_replay_frame(cls, frame: ReplayFrame) -> bytes:
        stream = MemoryStream()
        write_u8(stream, frame.button_state)
        write_boolean(stream, False)
        write_f32(stream, frame.mouse_x)
        write_f32(stream, frame.mouse_y)
        write_s32(stream, frame.time)
        return stream.data

    @classmethod
    def read_replay_frame(cls, stream: MemoryStream) -> ReplayFrame:
        frame = ReplayFrame()
        frame.button_state = ButtonState(read_u8(stream))
        legacy_mouse_right = read_boolean(stream)
        frame.mouse_x = read_f32(stream)
        frame.mouse_y = read_f32(stream)
        frame.time = read_s32(stream)

        if legacy_mouse_right:
            frame.button_state |= ButtonState.Right1

        return frame
