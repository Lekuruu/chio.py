
from typing import Iterable, Tuple
from .b1797 import b1797
from ..constants import *
from ..types import *
from ..io import *

class b1800(b1797):
    """
    b1800 deprecates the usage of gzip compression inside packets.
    """
    version = 1800

    @classmethod
    def write_packet(cls, stream: Stream, packet: PacketType, *args) -> None:
        if not packet.is_server_packet:
            raise ValueError(f"Packet '{packet.name}' is not a server packet")

        packet_writer = getattr(cls, packet.handler_name, None)

        if not packet_writer:
            return

        packets = packet_writer(*args)

        for packet, packet_data in packets:
            packet_id = cls.convert_output_packet(packet)
            compression_enabled = False
            write_u16(stream, packet_id)
            write_boolean(stream, compression_enabled)
            write_u32(stream, len(packet_data))
            stream.write(packet_data)
