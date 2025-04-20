
# Chio

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Lekuruu/chio.py/.github%2Fworkflows%2Fbuild.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chio)
![GitHub License](https://img.shields.io/github/license/Lekuruu/chio.py)

**Chio (Bancho I/O)** is a python library for serializing and deserializing bancho packets, with support for all versions of osu! that use bancho (2008-2025).

It was made with the intention of documenting everything about the bancho protocol, and to provide a base for server frameworks, since the packet handling part is most often the annoying part.  
Having *any* client be able to connect to it is a very sweet addition on top, if you are interested in those as well.

**If you wish to use this library, I would appreciate some credit for my work. Thanks!**

## Usage

This library requires an installation of python **3.8** or higher.  
You can install the library with pip:

```shell
pip install chio
```

Or you can also install it from source directly, if preferred:

```shell
pip install git+https://github.com/Lekuruu/chio.py
```

Here is a very basic example of how to use this library, and how to get a client to log in:

```python
import chio

# Chio expects you to have the `chio.Stream` class
# implemented, i.e. it needs a `read()` and `write()`
# function to work properly
stream = chio.Stream()

# The client version is how chio determines what
# protocol to use. This one can be parsed through the
# initial login request, that the client makes.
client_version = 20140127

# Chio has combined the user presence, stats and status
# into one class, to support more clients. You are also
# able to provide your own player class, as long as you
# have the same fields added on to it.
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

You can also read & write from bytes directly, for example when using HTTP clients instead of TCP clients:

```python
encoded = io.write_packet_to_bytes(chio.PacketType.BanchoLoginReply, info.id)
packet, data = io.read_packet_from_bytes(b"...")
```

If you are using **asyncio**, you may want to use the `read_packet_async` & `write_packet_async` functions respectively for asynchronous usage.
This feature is currently untested, but should work in theory. If you encounter any bugs with it, don't be afraid to report them.

```python
encoded = await io.write_packet_async(stream, chio.PacketType.BanchoLoginReply, info.id)
packet, data = await io.read_packet_async(stream)
```

### Patching

You are able to overwrite specifc packet readers/writers, with the `chio.patch` decorator.
As an example, to patch the `BanchoUserStats` packet inside of `b20120723`:

```python
@chio.patch(PacketType.BanchoUserStats, 20120723)
def write_user_stats(cls, info: UserInfo):
    stream = MemoryStream()
    write_s32(stream, info.id)
    stream.write(cls.write_status_update(info.status))
    write_u64(stream, info.stats.rscore)
    write_f32(stream, info.stats.accuracy)
    write_u32(stream, info.stats.playcount)
    write_u64(stream, info.stats.tscore)
    write_u32(stream, info.stats.rank)
    write_u16(stream, info.stats.pp)
    yield PacketType.BanchoUserStats, stream.data
```

Additionally, it's possible to set a certain slot size & protocol version for each version:

```python
# Set protocol version to 10 for b20120818
chio.set_protocol_version(10, 20120818)

# Override slot size to 32 for b20160404
chio.set_slot_size(32, 20160404)
```

### Datatypes

Depending on the packet you send or receive, you will need to account for different datatypes.  
Here is a list of them for each packet:

|             Packet             |                Type                 |
|:------------------------------:|:-----------------------------------:|
|         OsuUserStatus          |          `chio.UserStatus`          |
|           OsuMessage           |           `chio.Message`            |
|            OsuExit             |         `bool` (IsUpdating)         |
|     OsuStatusUpdateRequest     |                 N/A                 |
|            OsuPong             |                 N/A                 |
|        BanchoLoginReply        | `int` (UserId) or `chio.LoginError` |
|         BanchoMessage          |           `chio.Message`            |
|           BanchoPing           |                 N/A                 |
|    BanchoIrcChangeUsername     | `str` (old name), `str` (new name)  |
|         BanchoIrcQuit          |          `str` (Username)           |
|        BanchoUserStats         |           `chio.UserInfo`           |
|         BanchoUserQuit         |           `chio.UserQuit`           |
|     BanchoSpectatorJoined      |           `int` (UserId)            |
|      BanchoSpectatorLeft       |           `int` (UserId)            |
|      BanchoSpectateFrames      |      `chio.ReplayFrameBundle`       |
|       OsuStartSpectating       |           `int` (UserId)            |
|       OsuStopSpectating        |           `int` (UserId)            |
|       OsuSpectateFrames        |      `chio.ReplayFrameBundle`       |
|      BanchoVersionUpdate       |                 N/A                 |
|         OsuErrorReport         |          `str` (Exception)          |
|        OsuCantSpectate         |                 N/A                 |
|  BanchoSpectatorCantSpectate   |           `int` (UserId)            |
|       BanchoGetAttention       |                 N/A                 |
|         BanchoAnnounce         |           `str` (Message)           |
|       OsuPrivateMessage        |           `chio.Message`            |
|       BanchoMatchUpdate        |            `chio.Match`             |
|         BanchoMatchNew         |            `chio.Match`             |
|       BanchoMatchDisband       |           `int` (MatchId)           |
|          OsuLobbyPart          |                 N/A                 |
|          OsuLobbyJoin          |                 N/A                 |
|         OsuMatchCreate         |            `chio.Match`             |
|          OsuMatchJoin          |           `int` (MatchId)           |
|          OsuMatchPart          |                 N/A                 |
|        BanchoLobbyJoin         |           `int` (UserId)            |
|        BanchoLobbyPart         |           `int` (UserId)            |
|     BanchoMatchJoinSuccess     |            `chio.Match`             |
|      BanchoMatchJoinFail       |                 N/A                 |
|       OsuMatchChangeSlot       |           `int` (SlotId)            |
|         OsuMatchReady          |                 N/A                 |
|          OsuMatchLock          |           `int` (SlotId)            |
|     OsuMatchChangeSettings     |            `chio.Match`             |
|  BanchoFellowSpectatorJoined   |           `int` (UserId)            |
|   BanchoFellowSpectatorLeft    |           `int` (UserId)            |
|         OsuMatchStart          |                 N/A                 |
|        BanchoMatchStart        |            `chio.Match`             |
|      OsuMatchScoreUpdate       |          `chio.ScoreFrame`          |
|     BanchoMatchScoreUpdate     |          `chio.ScoreFrame`          |
|        OsuMatchComplete        |                 N/A                 |
|    BanchoMatchTransferHost     |                 N/A                 |
|       OsuMatchChangeMods       |             `chio.Mods`             |
|      OsuMatchLoadComplete      |                 N/A                 |
|  BanchoMatchAllPlayersLoaded   |                 N/A                 |
|       OsuMatchNoBeatmap        |                 N/A                 |
|        OsuMatchNotReady        |                 N/A                 |
|         OsuMatchFailed         |                 N/A                 |
|    BanchoMatchPlayerFailed     |           `int` (SlotId)            |
|      BanchoMatchComplete       |                 N/A                 |
|       OsuMatchHasBeatmap       |                 N/A                 |
|      OsuMatchSkipRequest       |                 N/A                 |
|        BanchoMatchSkip         |                 N/A                 |
|         OsuChannelJoin         |        `str` (Channel Name)         |
|    BanchoChannelJoinSuccess    |        `str` (Channel Name)         |
|     BanchoChannelAvailable     |           `chio.Channel`            |
|      BanchoChannelRevoked      |        `str` (Channel Name)         |
| BanchoChannelAvailableAutojoin |           `chio.Channel`            |
|     OsuBeatmapInfoRequest      |      `chio.BeatmapInfoRequest`      |
|     BanchoBeatmapInfoReply     |       `chio.BeatmapInfoReply`       |
|      OsuMatchTransferHost      |           `int` (SlotId)            |
|     BanchoLoginPermissions     |     `chio.Permissions` or `int`     |
|       BanchoFriendsList        |             `list[int]`             |
|         OsuFriendsAdd          |           `int` (UserId)            |
|        OsuFriendsRemove        |           `int` (UserId)            |
|   BanchoProtocolNegotiation    |            N/A or `int`             |
|       BanchoTitleUpdate        |         `chio.TitleUpdate`          |
|       OsuMatchChangeTeam       |                 N/A                 |
|        OsuChannelLeave         |        `str` (Channel Name)         |
|       OsuReceiveUpdates        |        `chio.PresenceFilter`        |
|         BanchoMonitor          |                 N/A                 |
|    BanchoMatchPlayerSkipped    |           `int` (SlotId)            |
|      OsuSetIrcAwayMessage      |           `chio.Message`            |
|       BanchoUserPresence       |           `chio.UserInfo`           |
|      OsuUserStatsRequest       |             `list[int]`             |
|         BanchoRestart          |  `int` (Retry After Milliseconds)   |
|           OsuInvite            |           `int` (UserId)            |
|          BanchoInvite          |           `chio.Message`            |
|     OsuMatchChangePassword     |            `chio.Match`             |
|   BanchoMatchChangePassword    |        `str` (New Password)         |
|       BanchoSilenceInfo        |    `int` (Locked Until Seconds)     |
|     OsuTournamentMatchInfo     |           `int` (MatchId)           |
|       BanchoUserSilenced       |           `int` (UserId)            |
|    BanchoUserPresenceSingle    |           `int` (UserId)            |
|    BanchoUserPresenceBundle    |        `list[int]` (UserIDs)        |
|       OsuPresenceRequest       |        `list[int]` (UserIDs)        |
|     OsuPresenceRequestAll      |                 N/A                 |
|     OsuChangeFriendOnlyDms     |      `bool` (Enabled/Disabled)      |
|      BanchoUserDmsBlocked      |           `chio.Message`            |
|     BanchoTargetIsSilenced     |           `chio.Message`            |
|   BanchoVersionUpdateForced    |                 N/A                 |
|       BanchoSwitchServer       |       `int` (After Idle Time)       |
|    BanchoAccountRestricted     |                 N/A                 |
|           BanchoRTX            |           `str` (Message)           |
|        BanchoMatchAbort        |                 N/A                 |
|  BanchoSwitchTournamentServer  |           `str` (Server)            |
| OsuTournamentJoinMatchChannel  |           `int` (MatchId)           |
| OsuTournamentLeaveMatchChannel |           `int` (MatchId)           |
