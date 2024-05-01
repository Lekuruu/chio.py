
from chio import RequestPacket, ResponsePacket
from chio.streams import StreamIn, StreamOut
from chio import versions
from typing import Any, Tuple

from .versions.reader import BaseReader
from .versions.writer import BaseWriter

from .versions import b20130815
from .versions import b20130329
from .versions import b20121223
from .versions import b20121119
from .versions import b20121008
from .versions import b20120812
from .versions import b20120725
from .versions import b20120704
from .versions import b1700
from .versions import b1150
from .versions import b675
from .versions import b590
from .versions import b553
from .versions import b535
from .versions import b503
from .versions import b483
from .versions import b399
from .versions import b388
from .versions import b338
from .versions import b337
from .versions import b323
from .versions import b319

import gzip

# TODO: Make this dynamic, based on the version
MULTIPLAYER_MAX_SLOTS = 8

def encode(version: int, packet: ResponsePacket, *objects) -> bytes:
    client_version = versions.get_next_version(version)
    packets = client_version.response_packets
    encoders = client_version.encoders

    stream = StreamOut()
    data = encoders[packet](*objects)

    if version <= 323:
        # In version 323 and below, the data is compressed by default
        data = gzip.compress(data)
        stream.legacy_header(packets[packet.name], len(data))
        stream.write(data)
        return stream.get()

    stream.header(packets[packet.name], len(data))
    stream.write(data)
    return stream.get()

def decode(version: int, data: bytes) -> Tuple[RequestPacket, Any]:
    client_version = versions.get_next_version(version)
    packets = client_version.request_packets
    decoders = client_version.decoders

    stream = StreamIn(data)
    packet_id = stream.u16()
    compression = True

    if version > 323:
        compression = stream.bool()

    payload = stream.read(stream.s32())

    if compression:
        # Gzip compression is only used in very old clients
        payload = gzip.decompress(payload)

    packet = packets(packet_id)
    decoder = decoders[packet]

    return packet, decoder(StreamIn(payload))
