
from typing import List, Any, Tuple
from gzip import compress

from ..errors import InvalidPacketError
from ..io import MemoryStream
from ..chio import BanchoIO
from ..constants import *
from ..types import *

class b282(BanchoIO):
    """
    b282 is the initial implementation of the bancho protocol.
    Every following version will be based on it.
    """
    version = 282

    def read_packet(self) -> Tuple[PacketType, Any]:
        packet_id = self.stream.read_u16()
        packet = self.convert_input_packet(packet_id)

        if not packet.is_client_packet:
            raise InvalidPacketError(f"Packet '{packet.name}' is not a client packet")

        packet_reader = getattr(self, packet.handler_name, None)

        if not packet_reader:
            raise InvalidPacketError(f"Version '{self.version}' does not implement packet '{packet.name}'")

        packet_length = self.stream.read_u32()
        packet_data = self.stream.read_gzip(packet_length)
        return packet, packet_reader(MemoryStream(packet_data))

    def write_packet(self, packet: PacketType, *args) -> None:
        if not packet.is_server_packet:
            raise InvalidPacketError(f"Packet '{packet.name}' is not a server packet")

        packet_writer = getattr(self, packet.handler_name, None)

        if not packet_writer:
            raise InvalidPacketError(f"Version '{self.version}' does not implement packet '{packet.name}'")

        packet, packet_data = compress(packet_writer(*args))

        if not packet_data:
            return

        packet_id = self.convert_output_packet(packet)
        self.stream.write_u16(packet_id)
        self.stream.write_u32(len(packet_data))
        self.stream.write(packet_data)

    def convert_input_packet(self, packet: int) -> PacketType:
        if packet == 11:
            # "IrcJoin" packet
            return PacketType.BanchoHandleIrcJoin

        if packet > 11 and packet <= 45:
            return PacketType(packet - 1)

        if packet > 50:
            return PacketType(packet - 1)

        return PacketType(packet)

    def convert_output_packet(self, packet: PacketType) -> int:
        if packet is PacketType.BanchoHandleIrcJoin:
            # "IrcJoin" packet
            return 11

        if packet.value >= 11 and packet.value < 45:
            return packet.value + 1

        if packet.value > 50:
            return packet.value + 1

        return packet.value

    def write_login_reply(self, reply: int) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_u32(reply)
        return PacketType.BanchoLoginReply, stream.data

    def write_ping(self) -> Tuple[PacketType, bytes]:
        return PacketType.BanchoPing, b""

    def write_message(self, message: Message) -> Tuple[PacketType, bytes]:
        if message.target != "#osu":
            # Private messages & channels have not been implemented yet
            return None, None

        stream = MemoryStream()
        stream.write_string(message.sender)
        stream.write_string(message.content)
        return PacketType.BanchoMessage, stream.data

    def write_irc_change_username(self, old_name: str, new_name: str) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_string(f"{old_name}>>>>{new_name}")
        return PacketType.BanchoIrcChangeUsername, stream.data

    def write_stats_update(self, info: UserInfo) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()

        if info.presence.is_irc:
            stream.write_string(info.name)
            return PacketType.BanchoHandleIrcJoin, stream.data

        stream.write_u32(info.id)
        stream.write_string(info.name)
        stream.write_u64(info.stats.rscore)
        stream.write_f64(info.stats.accuracy)
        stream.write_u32(info.stats.playcount)
        stream.write_u64(info.stats.tscore)
        stream.write_u32(info.stats.rank)
        stream.write_string(info.avatar_filename)
        stream.write(self.write_status_update(info.status))
        stream.write_u8(info.presence.timezone+24)
        stream.write_string(info.presence.city)
        return PacketType.BanchoStatsUpdate, stream.data
    
    def write_status_update(self, status: UserStatus) -> bytes:
        action = status.action if not status.update_stats else Status.StatsUpdate
        stream = MemoryStream()
        stream.write_u8(action.value)

        if action != Status.Unknown:
            stream.write_string(status.text)
            stream.write_string(status.beatmap_checksum)
            stream.write_u16(status.mods.value)

        return stream.data

    def write_user_quit(self, quit: UserQuit) -> Tuple[PacketType, bytes]:
        if quit.info.presence.is_irc and quit.quit_state != QuitState.IrcRemaining:
            stream = MemoryStream()
            stream.write_string(quit.info.name)
            return PacketType.BanchoIrcQuit, stream.data

        if quit.quit_state == QuitState.OsuRemaining:
            return None, None

        packet, data = self.write_stats_update(quit.info)
        packet = PacketType.BanchoUserQuit
        return packet, data
    
    def write_spectator_joined(self, user_id: int) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_u32(user_id)
        return PacketType.BanchoSpectatorJoined, stream.data

    def write_spectator_left(self, user_id: int) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_u32(user_id)
        return PacketType.BanchoSpectatorLeft, stream.data

    def write_spectate_frames(self, bundle: ReplayFrameBundle) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_u16(len(bundle.frames))

        for frame in bundle.frames:
            left_mouse = ButtonState.Left1 in frame.button_state or ButtonState.Left2 in frame.button_state
            right_mouse = ButtonState.Right1 in frame.button_state or ButtonState.Right2 in frame.button_state
            stream.write_boolean(left_mouse)
            stream.write_boolean(right_mouse)
            stream.write_f32(frame.mouse_x)
            stream.write_f32(frame.mouse_y)
            stream.write_s32(frame.time)

        stream.write_u8(bundle.action.value)
        return PacketType.BanchoSpectateFrames, stream.data

    def write_version_update(self) -> Tuple[PacketType, bytes]:
        return PacketType.BanchoVersionUpdate, b""

    def write_spectator_cant_spectate(self, user_id: int) -> Tuple[PacketType, bytes]:
        stream = MemoryStream()
        stream.write_u32(user_id)
        return PacketType.BanchoSpectatorCantSpectate, stream.data

    def write_user_presence(self, info: UserInfo) -> Tuple[PacketType, bytes]:
        # b282 does not support user presences,
        # instead we will send a stats update
        return self.write_stats_update(info)

    def write_user_presence_single(self, info: UserInfo) -> Tuple[PacketType, bytes]:
        return self.write_stats_update(info)

    def write_user_presence_bundle(self, infos: List[UserInfo]) -> Tuple[PacketType, bytes]:
        for info in infos:
            self.write_packet(PacketType.BanchoStatsUpdate, info)
        return None, None
    
    def read_user_status(self, stream: MemoryStream) -> UserStatus:
        status = UserStatus()
        status.action = Status(stream.read_u8())

        if status.action != Status.Unknown:
            status.text = stream.read_string()
            status.beatmap_checksum = stream.read_string()
            status.mods = Mods(stream.read_u16())

        return status
    
    def read_message(self, stream: MemoryStream) -> Message:
        # Private messages & channels have not been implemented yet
        return Message(
            content=stream.read_string(),
            target="#osu",
            sender=""
        )
    
    def read_spectate_frames(self, stream: MemoryStream) -> ReplayFrameBundle:
        frames = [
            self.read_replay_frame(stream)
            for _ in range(stream.read_u16())
        ]
        action = ReplayAction(stream.read_u8())
        return ReplayFrameBundle(action, frames)
    
    def read_replay_frame(self, stream: MemoryStream) -> ReplayFrame:
        frame = ReplayFrame()
        mouse_left = stream.read_boolean()
        mouse_right = stream.read_boolean()
        frame.mouse_x = stream.read_f32()
        frame.mouse_y = stream.read_f32()
        frame.time = stream.read_s32()

        if mouse_left:
            frame.button_state |= ButtonState.Left1
        if mouse_right:
            frame.button_state |= ButtonState.Right1

        return frame
