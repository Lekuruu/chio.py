
from chio.objects import bMatch

from .. import register_encoder
from . import ResponsePacket
from . import Writer

from typing import Callable

def register(packet: ResponsePacket) -> Callable:
    def wrapper(func) -> Callable:
        register_encoder(553, packet, func)
        register_encoder(536, packet, func)
        return func

    return wrapper

@register(ResponsePacket.NEW_MATCH)
def new_match(match: bMatch):
    writer = Writer()
    writer.write_match(match)
    return writer.stream.get()

@register(ResponsePacket.UPDATE_MATCH)
def update_match(match: bMatch):
    writer = Writer()
    writer.write_match(match)
    return writer.stream.get()

@register(ResponsePacket.MATCH_JOIN_SUCCESS)
def match_join_success(match: bMatch):
    writer = Writer()
    writer.write_match(match)
    return writer.stream.get()

@register(ResponsePacket.MATCH_START)
def match_start(match: bMatch):
    writer = Writer()
    writer.write_match(match)
    return writer.stream.get()
