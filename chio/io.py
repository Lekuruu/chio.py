
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

    def read_u8(self) -> int:
        return self.read(1)[0]
    
    def read_u16(self) -> int:
        return unpack(f"{self.endian}H", self.read(2))[0]
    
    def read_u32(self) -> int:
        return unpack(f"{self.endian}I", self.read(4))[0]
    
    def read_u64(self) -> int:
        return unpack(f"{self.endian}Q", self.read(8))[0]
    
    def read_boolean(self) -> bool:
        return bool(self.read_u8())

    def write_gzip(self, data: bytes) -> None:
        self.write(compress(data))

    def write_u8(self, value: int) -> None:
        self.write(pack(f"{self.endian}B", value))

    def write_u16(self, value: int) -> None:
        self.write(pack(f"{self.endian}H", value))

    def write_u32(self, value: int) -> None:
        self.write(pack(f"{self.endian}I", value))

    def write_u64(self, value: int) -> None:
        self.write(pack(f"{self.endian}Q", value))

    def write_boolean(self, value: bool) -> None:
        self.write_u8(int(value))

class MemoryStream(Stream):
    """
    Stream implementation that uses an in-memory buffer.
    """

    def __init__(self, data: bytes = b"", endian: str = "<") -> None:
        self.data = data
        self.position = 0
        self.endian = endian
        self.is_closed = False

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
