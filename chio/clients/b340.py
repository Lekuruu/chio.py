
from .b338 import b338
from ..constants import *
from ..types import *
from ..io import *

class b340(b338):
    """
    b340 removes the "MatchChangeBeatmap" packet, and introduces the "MatchHasBeatmap" packet.
    """
    version = 340

    @classmethod
    def convert_input_packet(cls, packet: int) -> PacketType:
        if packet == 11:
            # "IrcJoin" packet
            return PacketType.BanchoIrcJoin

        if packet > 11:
            packet -= 1

        return PacketType(packet)

    @classmethod
    def convert_output_packet(cls, packet: PacketType) -> int:
        if packet is PacketType.BanchoIrcJoin:
            # "IrcJoin" packet
            return 11

        if packet >= 11:
            return packet.value + 1

        return packet.value

    @classmethod
    def read_match_change_beatmap(cls, stream: MemoryStream) -> ...:
        ...

    @classmethod
    def read_match_has_beatmap(self, stream: MemoryStream) -> None:
        pass
