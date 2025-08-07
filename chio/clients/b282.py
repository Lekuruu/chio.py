
from typing import Any, Tuple, Iterable, Union

from ..chio import BanchoIO
from ..constants import *
from ..types import *
from ..io import *

class b282(BanchoIO):
    """
    b282 is the initial implementation of the bancho protocol.
    Every following version will be based on it.
    """
    version = 282

    @classmethod
    def read_packet(cls, stream: Stream) -> Tuple[PacketType, Any]:
        packet_id = read_u16(stream)
        packet = cls.convert_input_packet(packet_id)

        if not packet.is_client_packet:
            raise ValueError(f"Packet '{packet.name}' is not a client packet")

        packet_reader = getattr(cls, packet.handler_name, None)

        if not packet_reader:
            raise NotImplementedError(f"Version '{cls.version}' does not implement packet '{packet.name}'")

        packet_length = read_u32(stream)

        if packet_length >= packet.max_size:
            raise ValueError(f"Packet '{packet.name}' with length '{packet_length}' is too large")

        packet_data = read_gzip(stream, packet_length)
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
            packet_data = compress(packet_data)
            write_u16(output_stream, packet_id)
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
        
        packet_length = read_u32(input_stream)

        if packet_length >= packet.max_size:
            raise ValueError(f"Packet '{packet.name}' with length '{packet_length}' is too large")

        packet_data = await stream.read(packet_length)
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
            packet_data = compress(packet_data)
            write_u16(output_stream, packet_id)
            write_u32(output_stream, len(packet_data))
            output_stream.write(packet_data)
            await stream.write(output_stream.data)
            output_stream.clear()

    @classmethod
    def convert_input_packet(cls, packet: int) -> PacketType:
        """
        Convert a packet from the client to a modern packet
        type that can be handled by the server.
        """
        if packet == 11:
            # "IrcJoin" packet
            return PacketType.BanchoIrcJoin

        if 11 < packet <= 45:
            packet -= 1

        if packet > 50:
            packet -= 1

        return PacketType(packet)

    @classmethod
    def convert_output_packet(cls, packet: PacketType) -> int:
        """
        Convert a modern packet type from the server
        that the client can understand.
        """
        if packet is PacketType.BanchoIrcJoin:
            # "IrcJoin" packet
            return 11

        if 11 <= packet < 45:
            return packet.value + 1

        if packet > 50:
            return packet.value + 1

        return packet.value

    @classmethod
    def convert_input_status(cls, status: int) -> Status:
        if status == 10:
            return Status.Unknown

        if status > 9:
            return Status(status - 1)

        return Status(status)

    @classmethod
    def convert_output_status(cls, status: UserStatus) -> Status:
        if status.update_stats:
            return Status.StatsUpdate

        if status.action > 9:
            return Status(status.action.value - 1)

        return status.action

    @classmethod
    def format_chat_link(cls, text: str, url: str) -> str:
        return f"({text})[{url}]"

    @classmethod
    def write_login_reply(cls, reply: Union[int, LoginError]) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, reply)
        yield PacketType.BanchoLoginReply, stream.data

    @classmethod
    def write_ping(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoPing, b""

    @classmethod
    def write_message(cls, message: Message) -> Iterable[Tuple[PacketType, bytes]]:
        if message.target not in cls.autojoin_channels:
            # Private messages & channels have not been implemented yet
            return []

        stream = MemoryStream()
        write_string(stream, message.sender)
        write_string(stream, message.content_formatted)
        yield PacketType.BanchoMessage, stream.data

    @classmethod
    def write_irc_change_username(cls, old_name: str, new_name: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, f"{old_name}>>>>{new_name}")
        yield PacketType.BanchoIrcChangeUsername, stream.data

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_string(stream, info.name)
        write_u64(stream, info.stats.rscore)
        write_f64(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)
        write_string(stream, info.avatar_filename)
        stream.write(cls.write_status_update(info.status))
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.country_string)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_status_update(cls, status: UserStatus) -> bytes:
        action = cls.convert_output_status(status)
        stream = MemoryStream()
        write_u8(stream, action)

        if action != Status.Unknown:
            write_string(stream, status.text)
            write_string(stream, status.beatmap_checksum)
            write_u16(stream, status.mods)

        return stream.data

    @classmethod
    def write_user_quit(cls, quit: UserQuit) -> Iterable[Tuple[PacketType, bytes]]:
        if quit.info.presence.is_irc and quit.state != QuitState.IrcRemaining:
            stream = MemoryStream()
            write_string(stream, quit.info.name)
            return [(PacketType.BanchoIrcQuit, stream.data)]

        if quit.state == QuitState.OsuRemaining:
            return []

        packet, data = next(cls.write_user_stats(quit.info))
        packet = PacketType.BanchoUserQuit
        yield packet, data

    @classmethod
    def write_irc_join(cls, name: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, name)
        yield PacketType.BanchoIrcJoin, stream.data

    @classmethod
    def write_irc_quit(cls, name: str) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_string(stream, name)
        yield PacketType.BanchoIrcQuit, stream.data

    @classmethod
    def write_spectator_joined(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, user_id)
        yield PacketType.BanchoSpectatorJoined, stream.data

    @classmethod
    def write_spectator_left(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, user_id)
        yield PacketType.BanchoSpectatorLeft, stream.data

    @classmethod
    def write_spectate_frames(cls, bundle: ReplayFrameBundle) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u16(stream, len(bundle.frames))

        for frame in bundle.frames:
            stream.write(cls.write_replay_frame(frame))

        write_u8(stream, bundle.action)
        yield PacketType.BanchoSpectateFrames, stream.data

    @classmethod
    def write_replay_frame(cls, frame: ReplayFrame) -> bytes:
        stream = MemoryStream()
        left_mouse = ButtonState.Left1 in frame.button_state or ButtonState.Left2 in frame.button_state
        right_mouse = ButtonState.Right1 in frame.button_state or ButtonState.Right2 in frame.button_state
        write_boolean(stream, left_mouse)
        write_boolean(stream, right_mouse)
        write_f32(stream, frame.mouse_x)
        write_f32(stream, frame.mouse_y)
        write_s32(stream, frame.time)
        return stream.data

    @classmethod
    def write_version_update(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoVersionUpdate, b""

    @classmethod
    def write_spectator_cant_spectate(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_u32(stream, user_id)
        yield PacketType.BanchoSpectatorCantSpectate, stream.data

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        # b282 does not support user presences,
        # instead we will send a stats update
        return cls.write_user_stats(info)

    @classmethod
    def write_user_presence_single(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        return cls.write_user_presence(info)

    @classmethod
    def write_user_presence_bundle(cls, infos: List[UserInfo]) -> Iterable[Tuple[PacketType, bytes]]:
        for info in infos:
            for packet in cls.write_user_presence_single(info):
                yield packet

    @classmethod
    def write_invite(cls, invite_message: Message) -> Iterable[Tuple[PacketType, bytes]]:
        # b282 does not support invites, so instead
        # we will send the message directly
        return cls.write_message(invite_message)

    @classmethod
    def read_user_status(cls, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = cls.convert_input_status(read_u8(stream))

        if status.action != Status.Unknown:
            status.text = read_string(stream)
            status.beatmap_checksum = read_string(stream)
            status.mods = Mods(read_u16(stream))

        if status.action == Status.Idle and status.beatmap_checksum:
            # There is a bug where the client starts playing but
            # doesn't set the status to "Playing".
            status.action = Status.Playing

        return status

    @classmethod
    def read_message(cls, stream: MemoryStream) -> Message:
        # Private messages & channels have not been implemented yet
        return Message(
            content=read_string(stream),
            target="#osu",
            sender=""
        )

    @classmethod
    def read_exit(cls, stream: MemoryStream) -> bool:
        return False

    @classmethod
    def read_status_update_request(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_pong(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_start_spectating(cls, stream: MemoryStream) -> int:
        return read_s32(stream)

    @classmethod
    def read_stop_spectating(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_spectate_frames(cls, stream: MemoryStream) -> ReplayFrameBundle:
        frames = [
            cls.read_replay_frame(stream)
            for _ in range(read_u16(stream))
        ]
        action = ReplayAction(read_u8(stream))
        return ReplayFrameBundle(action, frames)

    @classmethod
    def read_replay_frame(cls, stream: MemoryStream) -> ReplayFrame:
        frame = ReplayFrame()
        mouse_left = read_boolean(stream)
        mouse_right = read_boolean(stream)
        frame.mouse_x = read_f32(stream)
        frame.mouse_y = read_f32(stream)
        frame.time = read_s32(stream)

        if mouse_left:
            frame.button_state |= ButtonState.Left1
        if mouse_right:
            frame.button_state |= ButtonState.Right1

        return frame

    @classmethod
    def read_error_report(cls, stream: MemoryStream) -> str:
        return read_string(stream)

    @classmethod
    def read_cant_spectate(cls, stream: MemoryStream) -> None:
        pass
