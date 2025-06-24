
from typing import Iterable, Tuple, Any
from .b323 import b323
from ..constants import *
from ..types import *
from ..io import *

class b334(b323):
    """
    b334 introduces a lot of breaking changes:
    - Compression boolean inside packet header
    - Removal of checksums in score frames
    - Mods inside match struct
    - Packet IDs 50-58
    """
    version = 334
    header_size = 7

    @classmethod
    def read_packet(cls, stream: Stream) -> Tuple[PacketType, Any]:
        packet_id = read_u16(stream)
        packet = cls.convert_input_packet(packet_id)

        if not packet.is_client_packet:
            raise ValueError(f"Packet '{packet.name}' is not a client packet")

        packet_reader = getattr(cls, packet.handler_name, None)

        if not packet_reader:
            raise NotImplementedError(f"Version '{cls.version}' does not implement packet '{packet.name}'")

        compression = read_boolean(stream)
        packet_length = read_u32(stream)

        if packet_length >= packet.max_size:
            raise ValueError(f"Packet '{packet.name}' with length '{packet_length}' is too large")        

        packet_data = stream.read(packet_length)

        if compression:
            packet_data = decompress(packet_data)

        return packet, packet_reader(MemoryStream(packet_data))

    @classmethod
    def write_packet(cls, stream: Stream, packet: PacketType, *args) -> None:
        if not packet.is_server_packet:
            raise ValueError(f"Packet '{packet.name}' is not a server packet")

        packet_writer = getattr(cls, packet.handler_name, None)

        if not packet_writer:
            return

        packets = packet_writer(*args)
        output_stream = MemoryStream()

        for packet, packet_data in packets:
            packet_id = cls.convert_output_packet(packet)
            compression_enabled = len(packet_data) > 150 and not cls.disable_compression

            if compression_enabled:
                packet_data = compress(packet_data)

            write_u16(output_stream, packet_id)
            write_boolean(output_stream, compression_enabled)
            write_u32(output_stream, len(packet_data))
            output_stream.write(packet_data)
            stream.write(output_stream.data)
            output_stream.clear()

    @classmethod
    async def read_packet_async(cls, stream: AsyncStream) -> Tuple[PacketType, Any]:
        input_stream = MemoryStream()
        input_stream.write(await stream.read(cls.header_size))

        packet_id = read_u16(input_stream)
        packet = cls.convert_input_packet(packet_id)

        if not packet.is_client_packet:
            raise ValueError(f"Packet '{packet.name}' is not a client packet")

        packet_reader = getattr(cls, packet.handler_name, None)

        if not packet_reader:
            raise NotImplementedError(f"Version '{cls.version}' does not implement packet '{packet.name}'")

        compression = read_boolean(input_stream)
        packet_length = read_u32(input_stream)

        if packet_length >= packet.max_size:
            raise ValueError(f"Packet '{packet.name}' with length '{packet_length}' is too large")

        packet_data = await stream.read(packet_length)

        if compression:
            packet_data = decompress(packet_data)

        return packet, packet_reader(MemoryStream(packet_data))

    @classmethod
    async def write_packet_async(cls, stream: AsyncStream, packet: PacketType, *args) -> None:
        if not packet.is_server_packet:
            raise ValueError(f"Packet '{packet.name}' is not a server packet")

        packet_writer = getattr(cls, packet.handler_name, None)

        if not packet_writer:
            return

        packets = packet_writer(*args)
        output_stream = MemoryStream()

        for packet, packet_data in packets:
            packet_id = cls.convert_output_packet(packet)
            compression_enabled = len(packet_data) > 150

            if compression_enabled:
                packet_data = compress(packet_data)

            write_u16(output_stream, packet_id)
            write_boolean(output_stream, compression_enabled)
            write_u32(output_stream, len(packet_data))
            output_stream.write(packet_data)
            await stream.write(output_stream.data)
            output_stream.clear()

    @classmethod
    def convert_input_packet(cls, packet: int) -> PacketType:
        if packet == 11:
            # "IrcJoin" packet
            return PacketType.BanchoIrcJoin
        
        if packet == 51:
            # "MatchChangeBeatmap" packet
            return PacketType.OsuMatchChangeBeatmap

        if packet > 11:
            packet -= 1

        if packet >= 51:
            packet -= 1

        return PacketType(packet)

    @classmethod
    def convert_output_packet(cls, packet: PacketType) -> int:
        if packet == PacketType.BanchoIrcJoin:
            # "IrcJoin" packet
            return 11

        if packet == PacketType.OsuMatchChangeBeatmap:
            # "MatchChangeBeatmap" packet
            return 51

        packet_id = packet.value

        if packet_id >= 11:
            packet_id += 1

        if packet_id >= 51:
            packet_id += 1

        return packet_id

    @classmethod
    def write_match_transfer_host(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchTransferHost, b''

    @classmethod
    def write_match_all_players_loaded(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchAllPlayersLoaded, b''

    @classmethod
    def write_match_player_failed(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoMatchPlayerFailed, stream.data

    @classmethod
    def write_match_complete(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchComplete, b''

    @classmethod
    def write_match_start(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchStart, cls.write_match(match)

    @classmethod
    def read_match_change_mods(cls, stream: MemoryStream) -> Mods:
        return Mods(read_s32(stream))

    @classmethod
    def read_match_load_complete(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_no_beatmap(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_not_ready(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_failed(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def write_score_frame(cls, stream: MemoryStream, frame: ScoreFrame) -> None:
        write_s32(stream, frame.time)
        write_u8(stream, frame.id)
        write_u16(stream, frame.total_300)
        write_u16(stream, frame.total_100)
        write_u16(stream, frame.total_50)
        write_u16(stream, frame.total_geki)
        write_u16(stream, frame.total_katu)
        write_u16(stream, frame.total_miss)
        write_u32(stream, frame.total_score)
        write_u16(stream, frame.max_combo)
        write_u16(stream, frame.current_combo)
        write_boolean(stream, frame.perfect)
        write_u8(stream, frame.hp)

    @classmethod
    def read_score_frame(cls, stream: MemoryStream) -> ScoreFrame:
        return ScoreFrame(
            time=read_s32(stream),
            id=read_u8(stream),
            total_300=read_u16(stream),
            total_100=read_u16(stream),
            total_50=read_u16(stream),
            total_geki=read_u16(stream),
            total_katu=read_u16(stream),
            total_miss=read_u16(stream),
            total_score=read_u32(stream),
            max_combo=read_u16(stream),
            current_combo=read_u16(stream),
            perfect=read_boolean(stream),
            hp=read_u8(stream),
            tag_byte=0
        )

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u8(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_u16(stream, match.mods.value)
        write_string(stream, match.name)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)

        for slot in match.slots:
            write_u8(stream, slot.status.value)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u8(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.mods = Mods(read_u16(stream))
        match.name = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)
        match.slots = [
            MatchSlot(status=SlotStatus(read_u8(stream)))
            for _ in range(cls.slot_size)
        ]

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        return match
