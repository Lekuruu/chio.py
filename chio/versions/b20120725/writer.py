
from ..b20120812 import Writer as BaseWriter

from chio.objects import bChannel

class Writer(BaseWriter):
    def write_channel(self, channel: bChannel):
        self.stream.string(channel.name)
