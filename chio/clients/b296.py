
from .b294 import b294
from ..constants import *
from ..types import *
from ..io import *

class b296(b294):
    """
    b296 adds the "Time" value to score frames.
    """
    version = 296

    @classmethod
    def write_score_frame(cls, stream: MemoryStream, frame: ScoreFrame) -> None:
        write_string(stream, frame.checksum)
        write_s32(stream, frame.time)
        write_u8(stream, frame.id)
        write_u16(stream, frame.total_300)
        write_u16(stream, frame.total_100)
        write_u16(stream, frame.total_50)
        write_u16(stream, frame.total_geki)
        write_u16(stream, frame.total_katu)
        write_u16(stream, frame.total_miss)
        write_u32(stream, frame.total_score)
        write_u16(stream, frame.max_combo)
        write_u16(stream, frame.current_combo)
        write_boolean(stream, frame.perfect)
        write_u8(stream, frame.hp)

    @classmethod
    def read_score_frame(cls, stream):
        # TODO: Validate checksum
        frame_checksum = read_string(stream)

        return ScoreFrame(
            time=read_s32(stream),
            id=read_u8(stream),
            total_300=read_u16(stream),
            total_100=read_u16(stream),
            total_50=read_u16(stream),
            total_geki=read_u16(stream),
            total_katu=read_u16(stream),
            total_miss=read_u16(stream),
            total_score=read_u32(stream),
            max_combo=read_u16(stream),
            current_combo=read_u16(stream),
            perfect=read_boolean(stream),
            hp=read_u8(stream),
            tag_byte=0
        )
