
from typing import Iterable, Tuple
from .b20151107 import b20151107
from ..constants import *
from ..types import *
from ..io import *

class b20160404(b20151107):
    """
    b20160404 adds a sequence number to the replay frame
    packet, to allow for replaying frames.
    """
    version = 20160404

    @classmethod
    def read_spectate_frames(cls, stream: MemoryStream) -> ReplayFrameBundle:
        if cls.protocol_version >= 18:
            extra = read_u32(stream)

        frames = [
            cls.read_replay_frame(stream)
            for _ in range(read_u16(stream))
        ]
        action = ReplayAction(read_u8(stream))
        frame = None

        if stream.available() > 2:
            frame = cls.read_score_frame(stream)

        sequence = read_u16(stream)
        return ReplayFrameBundle(action, frames, frame, extra, sequence)

    @classmethod
    def write_spectate_frames(cls, bundle: ReplayFrameBundle) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if cls.protocol_version >= 18:
            write_s32(stream, bundle.extra)

        write_u16(stream, len(bundle.frames))

        for frame in bundle.frames:
            stream.write(cls.write_replay_frame(frame))

        write_u8(stream, bundle.action)

        if bundle.frame:
            cls.write_score_frame(stream, bundle.frame)

        write_u16(stream, bundle.sequence or 0)
        yield PacketType.BanchoSpectateFrames, stream.data
