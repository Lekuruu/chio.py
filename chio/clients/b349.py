
from typing import Iterable, Tuple
from .b342 import b342
from ..constants import *
from ..types import *
from ..io import *

class b349(b342):
    """
    b349 adds the channel datatype and packets.
    """
    version = 349

    @classmethod
    def read_channel_join(cls, stream: MemoryStream) -> str:
        return read_string(stream)

    @classmethod
    def write_channel_join_success(cls, channel: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel)
        yield PacketType.BanchoChannelJoinSuccess, stream.data

    @classmethod
    def write_channel_revoked(cls, channel: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel)
        yield PacketType.BanchoChannelRevoked, stream.data

    @classmethod
    def write_channel_available(cls, channel: Channel) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel.name)
        yield PacketType.BanchoChannelAvailable, stream.data

    @classmethod
    def write_channel_available_autojoin(cls, channel: Channel) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, channel.name)
        yield PacketType.BanchoChannelAvailableAutojoin, stream.data
