
from typing import Iterable, Tuple
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
    def write_message(cls, message: Message) -> Iterable[Tuple[PacketType, bytes]]:
        if not message.is_direct_message and message.target not in cls.autojoin_channels:
            # Channel selection has not been implemented yet
            return []

        stream = MemoryStream()
        write_string(stream, message.sender)
        write_string(stream, message.content_formatted)
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
    def write_spectate_frames(cls, bundle: ReplayFrameBundle) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u16(stream, len(bundle.frames))

        for frame in bundle.frames:
            stream.write(cls.write_replay_frame(frame))

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
    def read_score_frame(cls, stream: MemoryStream) -> ScoreFrame:
        # TODO: Validate checksum
        frame_checksum = read_string(stream)

        return ScoreFrame(
            time=0,
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
