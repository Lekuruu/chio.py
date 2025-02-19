
from gzip import decompress, compress
from abc import ABC, abstractmethod
from struct import pack, unpack

class Stream(ABC):
    """
    Abstract class for I/O operations.
    """
    @property
    def endian(self) -> str:
        """
        Can be of the following values: '<', '>', '!', or '=' (default '<').
        """
        return "<"

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

class MemoryStream(Stream):
    """
    Stream implementation that uses an in-memory buffer.
    """

    def __init__(self, data: bytes = b"", endian: str = "<") -> None:
        self.data = data
        self.position = 0
        self.struct_endian = endian

    @property
    def endian(self) -> str:
        return self.struct_endian

    def read(self, size: int = -1) -> bytes:
        if size == -1:
            size = len(self.data) - self.position

        data = self.data[self.position:self.position + size]
        self.position += size
        return data

    def write(self, data: bytes) -> None:
        self.data += data

def read_s8(stream: Stream) -> int:
    return stream.read(1)[0]

def read_u8(stream: Stream) -> int:
    return stream.read(1)[0]

def read_u16(stream: Stream) -> int:
    return unpack(f"{stream.endian}H", stream.read(2))[0]

def read_s16(stream: Stream) -> int:
    return unpack(f"{stream.endian}h", stream.read(2))[0]

def read_u32(stream: Stream) -> int:
    return unpack(f"{stream.endian}I", stream.read(4))[0]

def read_s32(stream: Stream) -> int:
    return unpack(f"{stream.endian}i", stream.read(4))[0]

def read_u64(stream: Stream) -> int:
    return unpack(f"{stream.endian}Q", stream.read(8))[0]

def read_s64(stream: Stream) -> int:
    return unpack(f"{stream.endian}q", stream.read(8))[0]

def read_boolean(stream: Stream) -> bool:
    return bool(stream.read_u8())

def read_f32(stream: Stream) -> float:
    return unpack(f"{stream.endian}f", stream.read(4))[0]

def read_f64(stream: Stream) -> float:
    return unpack(f"{stream.endian}d", stream.read(8))[0]

def read_gzip(stream: Stream, size: int = -1) -> bytes:
    return decompress(stream.read(size))

def read_uleb128(stream: Stream) -> int:
    num = shift = 0

    while True:
        byte = stream.read_s8()
        num |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break

        shift += 7

    return num

def read_string(stream: Stream) -> str:
    empty = stream.read_s8() == 0x00

    if empty:
        return ""

    size = stream.read_uleb128()
    return stream.read(size).decode()

def write_s8(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}b", value))

def write_u8(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}B", value))

def write_s16(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}h", value))

def write_u16(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}H", value))

def write_s32(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}i", value))

def write_u32(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}I", value))

def write_s64(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}q", value))

def write_u64(stream: Stream, value: int) -> None:
    stream.write(pack(f"{stream.endian}Q", value))

def write_boolean(stream: Stream, value: bool) -> None:
    stream.write_u8(int(value))

def write_f32(stream: Stream, value: float) -> None:
    stream.write(pack(f"{stream.endian}f", value))

def write_f64(stream: Stream, value: float) -> None:
    stream.write(pack(f"{stream.endian}d", value))

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
        stream.write_s8(0x00)
        return

    string = value.encode()
    length = len(string)

    stream.write_s8(0x0b)
    stream.write_uleb128(length)
    stream.write(string)
