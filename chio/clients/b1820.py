
from typing import Iterable, Tuple
from .b1817 import b1817
from ..constants import *
from ..types import *
from ..io import *

class b1820(b1817):
    """
    b1820 adds the image url to the title update packet.
    """
    version = 1820

    @classmethod
    def write_title_update(cls, update: TitleUpdate) -> Iterable[Tuple[PacketType, bytes]]:
        if not update.image_url:
            return []

        stream = MemoryStream()
        write_string(stream, update.image_url)
        yield PacketType.BanchoTitleUpdate, stream.data
