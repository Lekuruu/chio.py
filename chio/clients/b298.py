
from typing import Tuple, Iterable
from .b296 import b296
from ..constants import *
from ..types import *
from ..io import *

class b298(b296):
    """
    b298 adds a partial implementation of multiplayer, as well as fellow spectators.
    """
    version = 298

    @classmethod
    def write_match_update(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        if match.id > 0xFF:
            # Match IDs greater than 255 are not supported in this client
            return []

        yield PacketType.BanchoMatchUpdate, cls.write_match(match)

    @classmethod
    def write_match_new(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        if match.id > 0xFF:
            # Match IDs greater than 255 are not supported in this client
            return []

        yield PacketType.BanchoMatchNew, cls.write_match(match)

    @classmethod
    def write_match_disband(cls, match_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, match_id)
        yield PacketType.BanchoMatchDisband, stream.data

    @classmethod
    def write_lobby_join(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoLobbyJoin, stream.data

    @classmethod
    def write_lobby_part(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoLobbyPart, stream.data

    @classmethod
    def write_match_join_success(cls, match: Match) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchJoinSuccess, cls.write_match(match)
    
    @classmethod
    def write_match_join_fail(cls) -> Iterable[Tuple[PacketType, bytes]]:
        yield PacketType.BanchoMatchJoinFail, b""

    @classmethod
    def write_fellow_spectator_joined(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        # Weirdly enough, the client seems to need both of these packets to be sent?
        # If only one is sent, the client will not display the fellow spectator.
        # yield PacketType.BanchoSpectatorJoined, stream.data
        yield PacketType.BanchoFellowSpectatorJoined, stream.data

    @classmethod
    def write_fellow_spectator_left(cls, user_id: int) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, user_id)
        yield PacketType.BanchoFellowSpectatorLeft, stream.data

    @classmethod
    def read_lobby_join(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_lobby_part(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_create(cls, stream: MemoryStream) -> Match:
        return cls.read_match(stream)

    @classmethod
    def read_match_join(cls, stream: MemoryStream) -> MatchJoin:
        return MatchJoin(read_s32(stream))

    @classmethod
    def read_match_part(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_change_slot(cls, stream: MemoryStream) -> int:
        return read_s32(stream)
    
    @classmethod
    def read_match_ready(cls, stream: MemoryStream) -> None:
        pass

    @classmethod
    def read_match_lock(cls, stream: MemoryStream) -> int:
        return read_s32(stream)

    @classmethod
    def read_match_change_settings(cls, stream: MemoryStream) -> Match:
        return cls.read_match(stream)

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        slots_open = [
            slot.status == SlotStatus.Open
            for slot in match.slots
        ]

        slots_used = [
            slot.has_player
            for slot in match.slots
        ]

        slots_ready = [
            slot.status == SlotStatus.Ready
            for slot in match.slots
        ]

        stream = MemoryStream()
        write_u8(stream, match.id)
        write_u8(stream, match.type)
        write_string(stream, match.name)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)
        write_bool_list(stream, slots_open)
        write_bool_list(stream, slots_used)
        write_bool_list(stream, slots_ready)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        return stream.data
    
    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u8(stream)
        match.type = MatchType(read_u8(stream))
        match.name = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)

        slots_open = read_bool_list(stream)
        slots_used = read_bool_list(stream)
        slots_ready = read_bool_list(stream)
        match.slots = []

        for i in range(cls.slot_size):
            slot = MatchSlot()
            slot.status = SlotStatus.Open if slots_open[i] else SlotStatus.Locked
            slot.status = SlotStatus.NotReady if slots_used[i] else slot.status
            slot.status = SlotStatus.Ready if slots_ready[i] else slot.status

            if slot.has_player:
                slot.user_id = read_s32(stream)

            match.slots.append(slot)

        return match
