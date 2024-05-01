
from typing import Callable

from chio.objects import (
    bUserInfo,
    bUserQuit
)

from .. import register_encoder
from . import ResponsePacket
from . import Writer

def register(packet: ResponsePacket) -> Callable:
    def wrapper(func) -> Callable:
        register_encoder(337, packet, func)
        register_encoder(334, packet, func)
        return func

    return wrapper

@register(ResponsePacket.USER_STATS)
def send_stats(info: bUserInfo):
    writer = Writer()
    writer.write_presence(info)
    return writer.stream.get()

@register(ResponsePacket.USER_QUIT)
def send_exit(user_quit: bUserQuit):
    writer = Writer()
    writer.write_quit(user_quit)
    return writer.stream.get()
