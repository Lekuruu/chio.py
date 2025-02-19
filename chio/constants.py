
from functools import cached_property
from enum import Enum, IntEnum
from re import compile

__all__ = [
    "PacketType",
    "Status",
    "Mode",
    "LoginError",
    "Permissions",
    "QuitState",
    "AvatarExtension",
    "PresenceFilter",
    "Completeness",
    "ReplayAction",
    "ButtonState",
    "Rank",
    "Mods",
    "MatchType",
    "ScoringType",
    "TeamType",
    "SlotStatus",
    "SlotTeam",
    "RankedStatus"
]

# Regex to convert camelCase to snake_case
# Example: "OsuSendUserStatus" -> "osu_send_user_status"
convert_pattern = compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

class PacketType(IntEnum):
    OsuUserStatus                  = 0
    OsuMessage                     = 1
    OsuExit                        = 2
    OsuStatusUpdateRequest         = 3
    OsuPong                        = 4
    BanchoLoginReply               = 5
    BanchoCommandError             = 6
    BanchoMessage                  = 7
    BanchoPing                     = 8
    BanchoIrcChangeUsername        = 9
    BanchoIrcQuit                  = 10
    BanchoUserStats                = 11
    BanchoUserQuit                 = 12
    BanchoSpectatorJoined          = 13
    BanchoSpectatorLeft            = 14
    BanchoSpectateFrames           = 15
    OsuStartSpectating             = 16
    OsuStopSpectating              = 17
    OsuSpectateFrames              = 18
    BanchoVersionUpdate            = 19
    OsuErrorReport                 = 20
    OsuCantSpectate                = 21
    BanchoSpectatorCantSpectate    = 22
    BanchoGetAttention             = 23
    BanchoAnnounce                 = 24
    OsuPrivateMessage              = 25
    BanchoMatchUpdate              = 26
    BanchoMatchNew                 = 27
    BanchoMatchDisband             = 28
    OsuLobbyPart                   = 29
    OsuLobbyJoin                   = 30
    OsuMatchCreate                 = 31
    OsuMatchJoin                   = 32
    OsuMatchPart                   = 33
    BanchoLobbyJoin                = 34
    BanchoLobbyPart                = 35
    BanchoMatchJoinSuccess         = 36
    BanchoMatchJoinFail            = 37
    OsuMatchChangeSlot             = 38
    OsuMatchReady                  = 39
    OsuMatchLock                   = 40
    OsuMatchChangeSettings         = 41
    BanchoFellowSpectatorJoined    = 42
    BanchoFellowSpectatorLeft      = 43
    OsuMatchStart                  = 44
    BanchoMatchStart               = 46
    OsuMatchScoreUpdate            = 47
    BanchoMatchScoreUpdate         = 48
    OsuMatchComplete               = 49
    BanchoMatchTransferHost        = 50
    OsuMatchChangeMods             = 51
    OsuMatchLoadComplete           = 52
    BanchoMatchAllPlayersLoaded    = 53
    OsuMatchNoBeatmap              = 54
    OsuMatchNotReady               = 55
    OsuMatchFailed                 = 56
    BanchoMatchPlayerFailed        = 57
    BanchoMatchComplete            = 58
    OsuMatchHasBeatmap             = 59
    OsuMatchSkipRequest            = 60
    BanchoMatchSkip                = 61
    BanchoUnauthorized             = 62
    OsuChannelJoin                 = 63
    BanchoChannelJoinSuccess       = 64
    BanchoChannelAvailable         = 65
    BanchoChannelRevoked           = 66
    BanchoChannelAvailableAutojoin = 67
    OsuBeatmapInfoRequest          = 68
    BanchoBeatmapInfoReply         = 69
    OsuMatchTransferHost           = 70
    BanchoLoginPermissions         = 71
    BanchoFriendsList              = 72
    OsuFriendsAdd                  = 73
    OsuFriendsRemove               = 74
    BanchoProtocolNegotiation      = 75
    BanchoTitleUpdate              = 76
    OsuMatchChangeTeam             = 77
    OsuChannelLeave                = 78
    OsuReceiveUpdates              = 79
    BanchoMonitor                  = 80
    BanchoMatchPlayerSkipped       = 81
    OsuSetIrcAwayMessage           = 82
    BanchoUserPresence             = 83
    OsuUserStatsRequest            = 85
    BanchoRestart                  = 86
    OsuInvite                      = 87
    BanchoInvite                   = 88
    BanchoChannelInfoComplete      = 89
    OsuMatchChangePassword         = 90
    BanchoMatchChangePassword      = 91
    BanchoSilenceInfo              = 92
    OsuTournamentMatchInfo         = 93
    BanchoUserSilenced             = 94
    BanchoUserPresenceSingle       = 95
    BanchoUserPresenceBundle       = 96
    OsuPresenceRequest             = 97
    OsuPresenceRequestAll          = 98
    OsuChangeFriendOnlyDMs         = 99
    BanchoUserDMsBlocked           = 100
    BanchoTargetIsSilenced         = 101
    BanchoVersionUpdateForced      = 102
    BanchoSwitchServer             = 103
    BanchoAccountRestricted        = 104
    BanchoRTX                      = 105
    BanchoMatchAbort               = 106
    BanchoSwitchTournamentServer   = 107
    OsuTournamentJoinMatchChannel  = 108
    OsuTournamentLeaveMatchChannel = 109

    # Packets that are unused today, but used in legacy clients
    BanchoIrcJoin         = 0xFFFF
    OsuMatchChangeBeatmap = 0xFFFE

    @cached_property
    def is_server_packet(self) -> bool:
        return self.name.startswith("Bancho")

    @cached_property
    def is_client_packet(self) -> bool:
        return self.name.startswith("Osu")

    @cached_property
    def handler_name(self) -> str:
        name = convert_pattern.sub("_", self.name).lower()
        name = name.replace("osu_", "read_")
        name = name.replace("bancho_", "write_")
        return name

class Status(IntEnum):
    Idle         = 0
    Afk          = 1
    Playing      = 2
    Editing      = 3
    Modding      = 4
    Multiplayer  = 5
    Watching     = 6
    Unknown      = 7
    Testing      = 8
    Submitting   = 9
    Paused       = 10
    Lobby        = 11
    Multiplaying = 12
    OsuDirect    = 13

    # Unused in later versions, but required for compatibility
    StatsUpdate = 10

class Mode(IntEnum):
    Osu   = 0
    Taiko = 1
    Catch = 2
    Mania = 3

class LoginError(IntEnum):
    InvalidLogin          = -1
    InvalidVersion        = -2
    UserBanned            = -3
    UserInactive          = -4
    ServerError           = -5
    UnauthorizedTestBuild = -6

class Permissions(IntEnum):
    NoPermissions = 0
    Regular       = 1 << 0
    BAT           = 1 << 1
    Supporter     = 1 << 2
    Friend        = 1 << 3
    Peppy         = 1 << 4
    Tournament    = 1 << 5

class QuitState(IntEnum):
    Gone         = 0
    OsuRemaining = 1
    IrcRemaining = 2

class AvatarExtension(IntEnum):
    Empty = 0
    Png   = 1
    Jpg   = 2

class PresenceFilter(IntEnum):
    NoPlayers = 0
    All       = 1
    Friends   = 2

class Completeness(IntEnum):
    StatusOnly = 0
    Statistics = 1
    Full       = 2

class ReplayAction(IntEnum):
    Standard      = 0
    NewSong       = 1
    Skip          = 2
    Completion    = 3
    Fail          = 4
    Pause         = 5
    Unpause       = 6
    SongSelect    = 7
    WatchingOther = 8

class ButtonState(IntEnum):
    NoButton = 0
    Left1    = 1 << 0
    Right1   = 1 << 1
    Left2    = 1 << 2
    Right2   = 1 << 3
    Smoke    = 1 << 4

class Rank(IntEnum):
    XH = 0
    SH = 1
    X  = 2
    S  = 3
    A  = 4
    B  = 5
    C  = 6
    D  = 7
    F  = 8
    N  = 9

class Mods(IntEnum):
    NoMod       = 0
    NoFail      = 1 << 0
    Easy        = 1 << 1
    NoVideo     = 1 << 2
    Hidden      = 1 << 3
    HardRock    = 1 << 4
    SuddenDeath = 1 << 5
    DoubleTime  = 1 << 6
    Relax       = 1 << 7
    HalfTime    = 1 << 8
    Nightcore   = 1 << 9
    Flashlight  = 1 << 10
    Autoplay    = 1 << 11
    SpunOut     = 1 << 12
    Autopilot   = 1 << 13
    Perfect     = 1 << 14
    Key4        = 1 << 15
    Key5        = 1 << 16
    Key6        = 1 << 17
    Key7        = 1 << 18
    Key8        = 1 << 19
    FadeIn      = 1 << 20
    Random      = 1 << 21
    Cinema      = 1 << 22
    Target      = 1 << 23
    Key9        = 1 << 24
    KeyCoop     = 1 << 25
    Key1        = 1 << 26
    Key3        = 1 << 27
    Key2        = 1 << 28
    ScoreV2     = 1 << 29
    Mirror      = 1 << 30

class MatchType(IntEnum):
    Standard  = 0
    Powerplay = 1

class ScoringType(IntEnum):
    Score    = 0
    Accuracy = 1
    Combo    = 2
    ScoreV2  = 3

class TeamType(IntEnum):
    HeadToHead = 0
    TagCoop    = 1
    TeamVs     = 2
    TagTeam    = 3

class SlotStatus(IntEnum):
    Open      = 1 << 0
    Locked    = 1 << 1
    NotReady  = 1 << 2
    Ready     = 1 << 3
    NoMap     = 1 << 4
    Playing   = 1 << 5
    Complete  = 1 << 6
    Quit      = 1 << 7
    HasPlayer = NotReady | Ready | NoMap | Playing | Complete

class SlotTeam(IntEnum):
    Neutral = 0
    Blue    = 1
    Red     = 2

class RankedStatus(IntEnum):
    Pending   = 0
    Ranked    = 1
    Approved  = 2
    Qualified = 3
