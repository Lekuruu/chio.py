
from typing import Iterable, Tuple
from .b312 import b312
from ..constants import *
from ..types import *
from ..io import *

class b320(b312):
    """
    b320 adds partial support for multiple channels
    """
    version = 320

    @classmethod
    def write_message(cls, message) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, message.sender)
        write_string(stream, message.content_formatted)
        write_string(stream, message.target)
        yield PacketType.BanchoMessage, stream.data

    @classmethod
    def read_message(cls, stream: MemoryStream) -> Message:
        return Message(
            sender=read_string(stream),
            content=read_string(stream),
            target=read_string(stream)
        )
    
    @classmethod
    def read_private_message(cls, stream: MemoryStream) -> Message:
        return cls.read_message(stream)
