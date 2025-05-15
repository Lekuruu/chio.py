
from typing import Any, Tuple, Iterable
from .io import Stream, MemoryStream, AsyncStream
from .constants import PacketType

class BanchoIO:
    """
    BanchoIO is an interface that wraps the basic methods for
    reading and writing packets to a Bancho client.
    """
    version: int = 0
    slot_size: int = 8
    header_size: int = 6
    protocol_version: int = 0
    disable_compression: bool = False
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
    async def read_packet_async(cls, stream: AsyncStream) -> Tuple[PacketType, Any]:
        """
        Reads a packet from the stream asynchronously, and returns the packet type and
        decoded data. The type of the decoded data depends on the received packet.
        """
        ...

    @classmethod
    async def write_packet_async(cls, stream: AsyncStream, packet: PacketType, *args) -> None:
        """
        Encodes a packet and writes it to the stream, asynchronously.
        """
        ...

    @classmethod
    def implements_packet(cls, packet: PacketType) -> bool:
        """
        Returns whether the current client version implements the given packet.
        """
        return getattr(cls, packet.handler_name, None) is not None

    @classmethod
    def read_packet_from_bytes(cls, data: bytes) -> Tuple[PacketType, Any]:
        """
        Reads a packet from the given bytes, and returns the packet type and decoded data.
        """
        stream = MemoryStream(data)
        return cls.read_packet(stream)

    @classmethod
    def read_many_packets_from_bytes(cls, data: bytes) -> Iterable[Tuple[PacketType, Any]]:
        """
        Reads multiple packets from the given bytes, and yields the packet type and decoded data.
        """
        stream = MemoryStream(data)

        while stream.available() >= cls.header_size:
            yield cls.read_packet(stream)

    @classmethod
    def write_packet_to_bytes(cls, packet: PacketType, *args) -> bytes:
        """
        Encodes a packet and returns it as bytes.
        """
        stream = MemoryStream()
        cls.write_packet(stream, packet, *args)
        return stream.data

    @classmethod
    def write_many_packets_to_bytes(cls, packets: Iterable[Tuple[PacketType, Any]]) -> bytes:
        """
        Encodes multiple packets and returns them as bytes.
        """
        stream = MemoryStream()

        for packet, *args in packets:
            cls.write_packet(stream, packet, *args)

        return stream.data
