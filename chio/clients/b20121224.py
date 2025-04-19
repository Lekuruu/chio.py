
from typing import Iterable, Tuple
from .b20121221 import b20121221
from ..constants import *
from ..types import *
from ..io import *

class b20121224(b20121221):
    """
    b20121224 deprecates the irc quit packet, in favor of a unified quit packet.
    Additionally it changes the way how user presences are sent to the client,
    when the client first joins the server, to reduce bandwidth usage.
    """
    version = 20121224

    @classmethod
    def write_user_quit(cls, quit: UserQuit) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_s32(stream, quit.info.id)
        write_u8(stream, quit.state)
        yield PacketType.BanchoUserQuit, stream.data

    @classmethod
    def write_user_presence_bundle(cls, infos: List[UserInfo]) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()
        write_list_s16(stream, [info.id for info in infos])
        yield PacketType.BanchoUserPresenceBundle, stream.data

    @classmethod
    def write_user_presence_single(cls, info):
        stream = MemoryStream()
        write_s32(stream, info.id)
        yield PacketType.BanchoUserPresenceSingle, stream.data

    @classmethod
    def read_presence_request(cls, stream: MemoryStream) -> List[int]:
        return read_list_s16(stream)

    @classmethod
    def read_presence_request_all(cls, stream: MemoryStream) -> None:
        pass
