from .b20150915 import b20150915
from ..types import *
from ..io import *

class b20151106(b20150915):
    """
    b20151106 adds scorev2-specific fields to the scoreframe packet.
    """
    version = 20151106

    @classmethod
    def write_score_frame(cls, stream: MemoryStream, frame: ScoreFrame) -> None:
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
        write_u8(stream, frame.tag_byte)
        write_boolean(stream, frame.using_scorev2)

        if frame.using_scorev2:
            write_f64(stream, frame.combo_portion)
            write_f64(stream, frame.bonus_portion)

    @classmethod
    def read_score_frame(cls, stream: MemoryStream) -> ScoreFrame:
        frame = ScoreFrame(
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
            tag_byte=read_u8(stream),
            using_scorev2=read_boolean(stream)
        )

        if frame.using_scorev2:
            frame.combo_portion = read_f64(stream)
            frame.bonus_portion = read_f64(stream)

        return frame
