
from typing import Iterable, Tuple
from .b20121212 import b20121212
from ..constants import *
from ..types import *
from ..io import *

class b20121221(b20121212):
    """
    b20121221 adds both the image url and redirect url to the title update packet.
    """
    version = 20121221

    @classmethod
    def write_title_update(cls, update: TitleUpdate) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, f"{update.image_url or ''}|{update.redirect_url or ''}")
        yield PacketType.BanchoTitleUpdate, stream.data
