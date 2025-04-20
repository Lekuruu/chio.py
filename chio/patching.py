
from typing import Callable
from functools import wraps
from .clients import ClientDict
from .constants import *

def patch(packet: PacketType, version: int) -> Callable:
    """
    Overwrite a packet handler for a specific protocol version.  
    For example, to overwrite the `BanchoUserStats` packet for b20120723:
    ```python
    @chio.patch(PacketType.BanchoUserStats, 20120723)
    def write_user_stats(cls, info: UserInfo):
        stream = MemoryStream()
        write_s32(stream, info.id)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)
        write_u16(stream, info.stats.pp)
        yield PacketType.BanchoUserStats, stream.data
    ```
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        client = ClientDict[version]
        setattr(client, packet.handler_name, wrapper)
        return wrapper
    return decorator

def set_protocol_version(protocol_version: int, version: int) -> None:
    """Override the protocol version for a specific client version."""
    client = ClientDict[version]
    client.protocol_version = protocol_version

def set_slot_size(slot_size: int, version: int) -> None:
    """Override the slot size for a specific client version."""
    client = ClientDict[version]
    client.slot_size = slot_size
