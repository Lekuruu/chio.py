
from chio.objects import bUserInfo

from .. import register_encoder
from . import ResponsePacket
from . import Writer

from typing import Callable

def register(packet: ResponsePacket) -> Callable:
    def wrapper(func) -> Callable:
        register_encoder(20121119, packet, func)
        register_encoder(20121030, packet, func)
        return func

    return wrapper

@register(ResponsePacket.USER_PRESENCE)
def presence(info: bUserInfo):
    writer = Writer()
    writer.write_presence(info)
    return writer.stream.get()
