
from gzip import decompress, compress
from abc import ABC, abstractmethod
from struct import pack, unpack

class Stream(ABC):
    """
    Abstract class for I/O operations.
    """
    @property
    @abstractmethod
    def endian(self) -> str:
        pass

    @abstractmethod
    def read(self, size: int = -1) -> bytes:
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def read_gzip(self, size: int = -1) -> bytes:
        return decompress(self.read(size))
    
    def read_s8(self) -> int:
        return self.read(1)[0]

    def read_u8(self) -> int:
        return self.read(1)[0]
    
    def read_u16(self) -> int:
        return unpack(f"{self.endian}H", self.read(2))[0]
    
    def read_s16(self) -> int:
        return unpack(f"{self.endian}h", self.read(2))[0]
    
    def read_u32(self) -> int:
        return unpack(f"{self.endian}I", self.read(4))[0]
    
    def read_s32(self) -> int:
        return unpack(f"{self.endian}i", self.read(4))[0]
    
    def read_u64(self) -> int:
        return unpack(f"{self.endian}Q", self.read(8))[0]
    
    def read_s64(self) -> int:
        return unpack(f"{self.endian}q", self.read(8))[0]

    def read_boolean(self) -> bool:
        return bool(self.read_u8())

    def read_f32(self) -> float:
        return unpack(f"{self.endian}f", self.read(4))[0]

    def read_f64(self) -> float:
        return unpack(f"{self.endian}d", self.read(8))[0]

    def read_uleb128(self) -> int:
        num = shift = 0

        while True:
            byte = self.read_s8()
            num |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:
                break

            shift += 7

        return num

    def read_string(self) -> str:
        empty = self.read_s8() == 0x00

        if empty:
            return ""

        size = self.read_uleb128()
        return self.read(size).decode()

    def write_gzip(self, data: bytes) -> None:
        self.write(compress(data))

    def write_s8(self, value: int) -> None:
        self.write(pack(f"{self.endian}b", value))

    def write_u8(self, value: int) -> None:
        self.write(pack(f"{self.endian}B", value))

    def write_s16(self, value: int) -> None:
        self.write(pack(f"{self.endian}h", value))

    def write_u16(self, value: int) -> None:
        self.write(pack(f"{self.endian}H", value))

    def write_s32(self, value: int) -> None:
        self.write(pack(f"{self.endian}i", value))

    def write_u32(self, value: int) -> None:
        self.write(pack(f"{self.endian}I", value))

    def write_s64(self, value: int) -> None:
        self.write(pack(f"{self.endian}q", value))

    def write_u64(self, value: int) -> None:
        self.write(pack(f"{self.endian}Q", value))

    def write_boolean(self, value: bool) -> None:
        self.write_u8(int(value))

    def write_f32(self, value: float) -> None:
        self.write(pack(f"{self.endian}f", value))

    def write_f64(self, value: float) -> None:
        self.write(pack(f"{self.endian}d", value))

    def write_uleb128(self, value: int) -> None:
        if value == 0:
            self.write(b'\x00')
            return

        ret = bytearray()

        while value != 0:
            ret.append(value & 0x7F)
            value >>= 7
            if value != 0:
                ret[-1] |= 0x80

        self.write(bytes(ret))

    def write_string(self, value: str) -> None:
        if not value:
            self.write_s8(0x00)
            return

        string = value.encode()
        length = len(string)

        self.write_s8(0x0b)
        self.write_uleb128(length)
        self.write(string)

class MemoryStream(Stream):
    """
    Stream implementation that uses an in-memory buffer.
    """

    def __init__(self, data: bytes = b"", endian: str = "<") -> None:
        self.data = data
        self.position = 0
        self.is_closed = False
        self.struct_endian = endian

    @property
    def endian(self) -> str:
        return self.struct_endian

    def read(self, size: int = -1) -> bytes:
        if self.is_closed:
            raise ValueError("Stream is closed")

        if size == -1:
            size = len(self.data) - self.position

        data = self.data[self.position:self.position + size]
        self.position += size
        return data

    def write(self, data: bytes) -> None:
        if self.is_closed:
            raise ValueError("Stream is closed")

        self.data += data

    def close(self) -> None:
        self.is_closed = True
