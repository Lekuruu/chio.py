
# Chio

Chio (Bancho I/O) is a python library for serializing and deserializing bancho packets, with support for all versions of osu!.
I will probably change the structure of the library in the near future, as I must admit that the code is pretty messy (but works at least). Once this "rewrite" is done, feel free to give me feedback on it.

## Usage

Install the library with pip:

```shell
pip install git+https://github.com/Lekuruu/chio.py.git
```

Encode & decode packets like this:

```python
from chio import ResponsePacket, RequestPacket
from chio.objects import bMessage
import chio

encoded = chio.encode(
    version=20130716,
    packet=ResponsePacket.SEND_MESSAGE,
    object=bMessage(
        "peppy",
        "Hello, World!",
        "#osu",
        sender_id=2
    )
)

print(f'Encoded Data: {encoded.hex()}')

packet, object = chio.decode(
    version=1700,
    data=bytes.fromhex(
        "010000200000000b0570657070790b0d48656c6c6f2c20576f726c64210b04236f737502000000"
    )
)

print(f'Packet: {packet.name}')
print(f'Data: {object}')
```
