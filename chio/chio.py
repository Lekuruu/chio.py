
from typing import List, Any, Tuple
from .constants import PacketType
from .io import Stream

class BanchoIO:
    """
    BanchoIO is an interface that wraps the basic methods for
    reading and writing packets to a Bancho client.
    """
    version: int = 0
    slot_size: int = 8
    header_size: int = 6
    protocol_version: int = 0
    requires_status_updates: bool = True

    @classmethod
    def read_packet(cls, stream: Stream) -> Tuple[PacketType, Any]:
        """
        Reads a packet from the stream, and returns the packet type and decoded data.
        The type of the decoded data depends on the received packet.
        """
        ...

    @classmethod
    def write_packet(cls, stream: Stream, packet: PacketType, *args) -> None:
        """
        Encodes a packet and writes it to the stream.
        """
        ...

    @classmethod
    def implements_packet(cls, packet: PacketType) -> bool:
        """
        Returns whether the current client version implements the given packet.
        """
        return getattr(cls, packet.handler_name, None) is not None
