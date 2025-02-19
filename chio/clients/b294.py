
from .b291 import b291
from ..constants import *
from ..types import *
from ..io import *

class b294(b291):
    """
    b294 implements private messages, as well as score frames in spectating.
    """
    version = 294

    @classmethod
    def write_message(cls, message: Message):
        if not message.is_direct_message and message.target != "#osu":
            # Channel selection has not been implemented yet
            return []

        stream = MemoryStream()
        write_string(stream, message.sender)
        write_string(stream, message.content)
        write_boolean(stream, message.is_direct_message)
        yield PacketType.BanchoMessage, stream.data

    @classmethod
    def read_message(cls, stream: MemoryStream):
        # Channel selection has not been implemented yet
        return Message(
            content=read_string(stream),
            target="#osu",
            sender=""
        )

    @classmethod
    def read_private_message(cls, stream: MemoryStream) -> Message:
        target = read_string(stream)
        content = read_string(stream)
        is_direct_message = read_boolean(stream)

        if not is_direct_message:
            raise ValueError("Expected direct message, got channel message")

        return Message("", content, target)

    @classmethod
    def write_spectate_frames(cls, bundle: ReplayFrameBundle):
        stream = MemoryStream()
        write_u16(stream, len(bundle.frames))

        for frame in bundle.frames:
            left_mouse = ButtonState.Left1 in frame.button_state or ButtonState.Left2 in frame.button_state
            right_mouse = ButtonState.Right1 in frame.button_state or ButtonState.Right2 in frame.button_state
            write_boolean(stream, left_mouse)
            write_boolean(stream, right_mouse)
            write_f32(stream, frame.mouse_x)
            write_f32(stream, frame.mouse_y)
            write_s32(stream, frame.time)

        write_u8(stream, bundle.action)

        if bundle.frame:
            cls.write_score_frame(stream, bundle.frame)

        yield PacketType.BanchoSpectateFrames, stream.data

    @classmethod
    def read_spectate_frames(cls, stream: MemoryStream) -> ReplayFrameBundle:
        frames = [
            cls.read_replay_frame(stream)
            for _ in range(read_u16(stream))
        ]
        action = ReplayAction(read_u8(stream))
        frame = None

        if stream.available() > 0:
            frame = cls.read_score_frame(stream)

        return ReplayFrameBundle(action, frames, frame)

    @classmethod
    def write_score_frame(cls, stream: MemoryStream, frame: ScoreFrame) -> None:
        write_string(stream, frame.checksum)
        write_u8(stream, frame.id)
        write_u16(stream, frame.count_300)
        write_u16(stream, frame.count_100)
        write_u16(stream, frame.count_50)
        write_u16(stream, frame.count_geki)
        write_u16(stream, frame.count_katu)
        write_u16(stream, frame.count_miss)
        write_u32(stream, frame.total_score)
        write_u16(stream, frame.max_combo)
        write_u16(stream, frame.current_combo)
        write_boolean(stream, frame.perfect)
        write_u8(stream, frame.hp)

    @classmethod
    def read_score_frame(cls, stream: MemoryStream) -> ScoreFrame:
        return ScoreFrame(
            checksum=read_string(stream),
            id=read_u8(stream),
            count_300=read_u16(stream),
            count_100=read_u16(stream),
            count_50=read_u16(stream),
            count_geki=read_u16(stream),
            count_katu=read_u16(stream),
            count_miss=read_u16(stream),
            total_score=read_u32(stream),
            max_combo=read_u16(stream),
            current_combo=read_u16(stream),
            perfect=read_boolean(stream),
            hp=read_u8(stream)
        )
