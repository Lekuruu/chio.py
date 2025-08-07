
from typing import Iterable, Tuple

from .b20121211 import b20121211
from ..constants import *
from ..io import *

class b20121212(b20121211):
    """
    b20121212 adds support for the user silenced packet & changes the chat link format.
    """
    version = 20121212

    @classmethod
    def format_chat_link(cls, text: str, url: str) -> str:
        return f"[{url} {text}]"

    @classmethod
    def write_user_silenced(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoUserSilenced, stream.data
