
from gzip import decompress, compress
from abc import ABC, abstractmethod
from struct import pack, unpack
from typing import List

import traceback
import logging

class Stream(ABC):
    """
    Abstract class for I/O operations.
    """
    @abstractmethod
    def read(self, size: int = -1) -> bytes:
        """
        Read a number of bytes from the stream.
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """
        Write a number of bytes to the stream.
        """
        pass

class AsyncStream(ABC):
    """
    Abstract class for asynchronous I/O operations.
    """
    @abstractmethod
    async def read(self, size: int = -1) -> bytes:
        """
        Read a number of bytes from the stream asynchronously.
        """
        pass

    @abstractmethod
    async def write(self, data: bytes) -> None:
        """
        Write a number of bytes to the stream asynchronously.
        """
        pass

class MemoryStream(Stream):
    """
    Stream implementation that uses an in-memory buffer.
    """

    def __init__(self, data: bytes = b"", endian: str = "<") -> None:
        self.data = data
        self.position = 0
        self.struct_endian = endian

    def __del__(self):
        self.clear()

    @property
    def endian(self) -> str:
        return self.struct_endian

    def write(self, data: bytes) -> None:
        self.data += data

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            size = len(self.data) - self.position

        data = self.data[self.position:self.position + size]
        self.position += size
        return data
    
    def clear(self) -> None:
        self.data = b""
        self.position = 0

    def available(self) -> int:
        return len(self.data) - self.position

logger = logging.getLogger('chio.py')

def clamp(value: int, min_value: int, max_value: int) -> int:
    clamped = max(min_value, min(value, max_value))

    if clamped != value:
        stack = traceback.extract_stack()
        caller = stack[-3]
        logger.warning(
            f"Value '{value}' was clamped to '{clamped}' "
            f"({caller.filename}:{caller.lineno} in '{caller.name}')"
        )

    return clamped

def read_s8(stream: Stream) -> int:
    return stream.read(1)[0]

def read_u8(stream: Stream) -> int:
    return stream.read(1)[0]

def read_u16(stream: Stream) -> int:
    return unpack("<H", stream.read(2))[0]

def read_s16(stream: Stream) -> int:
    return unpack("<h", stream.read(2))[0]

def read_u32(stream: Stream) -> int:
    return unpack("<I", stream.read(4))[0]

def read_s32(stream: Stream) -> int:
    return unpack("<i", stream.read(4))[0]

def read_u64(stream: Stream) -> int:
    return unpack("<Q", stream.read(8))[0]

def read_s64(stream: Stream) -> int:
    return unpack("<q", stream.read(8))[0]

def read_boolean(stream: Stream) -> bool:
    return bool(read_u8(stream))

def read_f32(stream: Stream) -> float:
    return unpack("<f", stream.read(4))[0]

def read_f64(stream: Stream) -> float:
    return unpack("<d", stream.read(8))[0]

def read_gzip(stream: Stream, size: int = -1) -> bytes:
    return decompress(stream.read(size))

def read_uleb128(stream: Stream) -> int:
    num = shift = 0

    while True:
        byte = read_s8(stream)
        num |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break

        shift += 7

    return num

def read_string(stream: Stream) -> str:
    empty = read_s8(stream) == 0x00

    if empty:
        return ""

    size = read_uleb128(stream)
    return stream.read(size).decode()

def read_bool_list(stream: Stream, size: int = 8) -> List[bool]:
    byte = read_u8(stream)
    return [((byte >> index) & 1) > 0 for index in range(size)]

def read_list_s32(stream: Stream) -> List[int]:
    return [read_s32(stream) for _ in range(read_s32(stream))]

def read_list_s16(stream: Stream) -> List[int]:
    return [read_s32(stream) for _ in range(read_u16(stream))]

def write_s8(stream: Stream, value: int) -> None:
    stream.write(pack("<b", clamp(value, -0x80, 0x7F)))

def write_u8(stream: Stream, value: int) -> None:
    stream.write(pack("<B", clamp(value, 0x00, 0xFF)))

def write_s16(stream: Stream, value: int) -> None:
    stream.write(pack("<h", clamp(value, -0x8000, 0x7FFF)))

def write_u16(stream: Stream, value: int) -> None:
    stream.write(pack("<H", clamp(value, 0x0000, 0xFFFF)))

def write_s32(stream: Stream, value: int) -> None:
    stream.write(pack("<i", clamp(value, -0x80000000, 0x7FFFFFFF)))

def write_u32(stream: Stream, value: int) -> None:
    stream.write(pack("<I", clamp(value, 0x00000000, 0xFFFFFFFF)))

def write_s64(stream: Stream, value: int) -> None:
    stream.write(pack("<q", clamp(value, -0x8000000000000000, 0x7FFFFFFFFFFFFFFF)))

def write_u64(stream: Stream, value: int) -> None:
    stream.write(pack("<Q", clamp(value, 0x0000000000000000, 0xFFFFFFFFFFFFFFFF)))

def write_boolean(stream: Stream, value: bool) -> None:
    write_u8(stream, int(bool(value)))

def write_f32(stream: Stream, value: float) -> None:
    stream.write(pack("<f", value))

def write_f64(stream: Stream, value: float) -> None:
    stream.write(pack("<d", value))

def write_gzip(stream: Stream, data: bytes) -> None:
    stream.write(compress(data))

def write_uleb128(stream: Stream, value: int) -> None:
    if value == 0:
        stream.write(b'\x00')
        return

    ret = bytearray()

    while value != 0:
        ret.append(value & 0x7F)
        value >>= 7
        if value != 0:
            ret[-1] |= 0x80

    stream.write(bytes(ret))

def write_string(stream: Stream, value: str) -> None:
    if not value:
        write_s8(stream, 0x00)
        return

    string = value.encode()
    length = len(string)

    write_s8(stream, 0x0b)
    write_uleb128(stream, length)
    stream.write(string)

def write_bool_list(stream: Stream, values: List[bool]) -> None:
    byte = 0

    for index in range(len(values)-1, -1, -1):
        if values[index]:
            byte |= 1
        if index > 0:
            byte = byte << 1

    write_u8(stream, byte)

def write_list_s32(stream: Stream, values: List[int]) -> None:
    write_s32(stream, len(values))

    for value in values:
        write_s32(stream, value)

def write_list_s16(stream: Stream, values: List[int]) -> None:
    write_u16(stream, len(values))

    for value in values:
        write_s32(stream, value)
