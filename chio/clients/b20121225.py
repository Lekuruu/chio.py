
from typing import Iterable, Tuple
from .b20121224 import b20121224
from ..constants import *
from ..types import *
from ..io import *

class b20121225(b20121224):
    """
    b20121225 adds the user ID of the message sender to the message packet, so
    that the client can request the user's presence, if it's not available.
    """
    version = 20121225
    protocol_version = 15

    @classmethod
    def write_message(cls, message: Message) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message.sender)
        write_string(stream, message.content)
        write_string(stream, message.target)

        if cls.protocol_version >= 15:
            write_s32(stream, message.sender_id)

        yield PacketType.BanchoMessage, stream.data

    @classmethod
    def read_message(cls, stream: MemoryStream) -> Message:
        message = Message(
            sender=read_string(stream),
            content=read_string(stream),
            target=read_string(stream)
        )

        if cls.protocol_version >= 15:
            message.sender_id = read_s32(stream)

        return message
