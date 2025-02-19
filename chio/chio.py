
from typing import List, Any, Tuple
from dataclasses import dataclass
from .constants import PacketType
from .io import Stream

@dataclass
class BanchoIO:
    """
    BanchoIO is an interface that wraps the basic methods for
    reading and writing packets to a Bancho client.
    """
    stream: Stream
    version: int = 0
    slot_size: int = 8

    def read_packet(self) -> Tuple[PacketType, Any]:
        """
        Reads a packet from the stream, and returns the packet type and decoded data.
        The type of the decoded data depends on the received packet.
        """
        ...

    def write_packet(self, packet: PacketType, data: Any) -> None:
        """
        Encodes a packet and writes it to the stream.
        """
        ...

    def implements_packet(self, packet: PacketType) -> bool:
        """
        Returns whether the current client version implements the given packet.
        """
        return getattr(self, packet.handler_name, None) is not None
