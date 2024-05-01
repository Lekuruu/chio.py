
from chio.objects import bUserInfo
from typing import Callable

from .. import register_encoder
from . import ResponsePacket
from . import Writer

def register(packet: ResponsePacket) -> Callable:
    def wrapper(func) -> Callable:
        register_encoder(1150, packet, func)
        register_encoder(679, packet, func)
        return func

    return wrapper

@register(ResponsePacket.LOGIN_REPLY)
def send_login_reply(reply: int):
    if reply < -3:
        # Login Errors < -3 are not supported
        reply = -1

    return int(reply).to_bytes(
        length=4,
        byteorder='little',
        signed=True
    )

@register(ResponsePacket.USER_STATS)
def send_stats(info: bUserInfo):
    writer = Writer()
    writer.write_presence(info)
    return writer.stream.get()
