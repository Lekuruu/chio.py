
from typing import Iterable, Tuple
from .b20120723 import b20120723
from ..constants import *
from ..types import *
from ..io import *

class b20120725(b20120723):
    """
    b20120725 now displays the topic & user count of a channel in the channel listing.
    """
    version = 20120725
    protocol_version = 9

    @classmethod
    def write_channel_available(cls, channel: Channel) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel.name)

        if cls.protocol_version >= 9:
            write_string(stream, channel.topic)
            write_s16(stream, channel.user_count)

        yield PacketType.BanchoChannelAvailable, stream.data

    @classmethod
    def write_channel_available_autojoin(cls, channel: Channel) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel.name)

        if cls.protocol_version >= 9:
            write_string(stream, channel.topic)
            write_s16(stream, channel.user_count)

        yield PacketType.BanchoChannelAvailableAutojoin, stream.data
