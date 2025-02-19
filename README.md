
# Chio

Chio (Bancho I/O) is a python library for serializing and deserializing bancho packets, with support for (almost) all versions of osu!.

## Usage

This branch is currently under heavy development, but here is how the future package may look:

```python
import chio

# Assuming you got a client already connected
client_stream = ...
client_version = 282

info = chio.UserInfo(
    id=2,
    name="Levi",
    presence=chio.UserPresence(
        is_irc=False,
        timezone=0,
        country_index=0,
        permissions=Permissions.Regular|Permissions.Supporter,
        longitude=0,
        latitude=0,
        city="idk, figure it out yourself",
    ),
    stats=chio.UserStats(
        rank=1,
        rscore=245768,
        tscore=46794679,
        accuracy=0.99367,
        playcount=69,
        pp=4200,
    ),
    status=chio.UserStatus()
)

io = chio.select_client(client_version)
io.write_packet(chio.PacketType.BanchoLoginReply, info.id)
io.write_packet(chio.PacketType.BanchoUserPresence, info)
io.write_packet(chio.PacketType.BanchoUserStats, info)
io.write_packet(
    chio.PacketType.BanchoMessage,
    chio.Message(content="Hello, World!", sender="BanchoBot", target="#osu")
)

packet, data = self.io.read_packet(client_stream)
print(f"Received packet '{packet.name}' with {data}.")
```
