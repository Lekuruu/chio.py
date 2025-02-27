
# Chio

Chio (Bancho I/O) is a python library for serializing and deserializing bancho packets, with support for all versions of osu! that use bancho (2008-2025).

## Usage

Install the library with pip:
```shell
pip install chio
```

Also installable from source directly, if preferred:
```shell
pip install git+https://github.com/Lekuruu/chio.py
```

```python
import chio

# Chio expects you to have the `chio.Stream` class
# implemented, i.e. it needs a `read()` and `write()`
# function to work properly
stream = chio.Stream()

# The client version is how chio determines what
# protocol to use. This one can be parsed through the
# initial login request, that the client makes.
client_version = 282

info = chio.UserInfo(
    id=2,
    name="peppy",
    presence=chio.UserPresence(),
    stats=chio.UserStats(),
    status=chio.UserStatus()
)

# Select a client protocol to use for encoding/decoding
io = chio.select_client(client_version)

# Send the users information (userId, presence & stats)
io.write_packet(stream, chio.PacketType.BanchoLoginReply, info.id)
io.write_packet(stream, chio.PacketType.BanchoUserPresence, info)
io.write_packet(stream, chio.PacketType.BanchoUserStats, info)

# Force client to join #osu
io.write_packet(stream, chio.PacketType.BanchoChannelJoinSuccess, "#osu")

# Send a message in #osu from BanchoBot
io.write_packet(
    stream,
    chio.PacketType.BanchoMessage,
    chio.Message(content="Hello, World!", sender="BanchoBot", target="#osu")
)

packet, data = io.read_packet(stream)
print(f"Received packet '{packet.name}' with {data}.")
```

You can also read & write from bytes directly, for example when using HTTP clients instead of TCP clients.
```python
encoded = io.write_packet_to_bytes(chio.PacketType.BanchoLoginReply, info.id)
packet, data = io.read_packet_from_bytes(b"...")
```
