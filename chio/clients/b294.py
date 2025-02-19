
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
