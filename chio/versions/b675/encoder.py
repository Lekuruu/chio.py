
from typing import Callable, Optional
from chio.objects import bUserInfo

from .. import register_encoder
from . import ResponsePacket
from . import Writer

def register(packet: ResponsePacket) -> Callable:
    def wrapper(func) -> Callable:
        register_encoder(675, packet, func)
        register_encoder(591, packet, func)
        return func

    return wrapper

@register(ResponsePacket.USER_STATS)
def send_stats(info: bUserInfo):
    writer = Writer()
    writer.write_presence(info)
    return writer.stream.get()
