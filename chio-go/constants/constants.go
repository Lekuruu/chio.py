package constants

import (
	"regexp"
	"strings"
)

// Regex to convert camelCase to snake_case
// Example: "OsuSendUserStatus" -> "osu_send_user_status"
var CaseConvertPattern = regexp.MustCompile(`([a-z])([A-Z])|([A-Z])([A-Z][a-z])`)

// Chat link regex patterns:
// Modern: [http://example.com Example]
// Legacy: (Example)[http://example.com]
var ChatLinkModern = regexp.MustCompile(`\[((?:https?:\/\/)[^\s\]]+)\s+((?:[^\[\]]|\[[^\[\]]*\])*)\]`)
var ChatLinkLegacy = regexp.MustCompile(`\[([^\]]+)\]\((https?:\/\/[^)]+)\)`)

// PacketType represents the type of packet in the Bancho protocol
type PacketType int

const (
	OsuUserStatus                  PacketType = 0
	OsuMessage                     PacketType = 1
	OsuExit                        PacketType = 2
	OsuStatusUpdateRequest         PacketType = 3
	OsuPong                        PacketType = 4
	BanchoLoginReply               PacketType = 5
	BanchoCommandError             PacketType = 6
	BanchoMessage                  PacketType = 7
	BanchoPing                     PacketType = 8
	BanchoIrcChangeUsername        PacketType = 9
	BanchoIrcQuit                  PacketType = 10
	BanchoUserStats                PacketType = 11
	BanchoUserQuit                 PacketType = 12
	BanchoSpectatorJoined          PacketType = 13
	BanchoSpectatorLeft            PacketType = 14
	BanchoSpectateFrames           PacketType = 15
	OsuStartSpectating             PacketType = 16
	OsuStopSpectating              PacketType = 17
	OsuSpectateFrames              PacketType = 18
	BanchoVersionUpdate            PacketType = 19
	OsuErrorReport                 PacketType = 20
	OsuCantSpectate                PacketType = 21
	BanchoSpectatorCantSpectate    PacketType = 22
	BanchoGetAttention             PacketType = 23
	BanchoAnnounce                 PacketType = 24
	OsuPrivateMessage              PacketType = 25
	BanchoMatchUpdate              PacketType = 26
	BanchoMatchNew                 PacketType = 27
	BanchoMatchDisband             PacketType = 28
	OsuLobbyPart                   PacketType = 29
	OsuLobbyJoin                   PacketType = 30
	OsuMatchCreate                 PacketType = 31
	OsuMatchJoin                   PacketType = 32
	OsuMatchPart                   PacketType = 33
	BanchoLobbyJoin                PacketType = 34
	BanchoLobbyPart                PacketType = 35
	BanchoMatchJoinSuccess         PacketType = 36
	BanchoMatchJoinFail            PacketType = 37
	OsuMatchChangeSlot             PacketType = 38
	OsuMatchReady                  PacketType = 39
	OsuMatchLock                   PacketType = 40
	OsuMatchChangeSettings         PacketType = 41
	BanchoFellowSpectatorJoined    PacketType = 42
	BanchoFellowSpectatorLeft      PacketType = 43
	OsuMatchStart                  PacketType = 44
	BanchoMatchStart               PacketType = 46
	OsuMatchScoreUpdate            PacketType = 47
	BanchoMatchScoreUpdate         PacketType = 48
	OsuMatchComplete               PacketType = 49
	BanchoMatchTransferHost        PacketType = 50
	OsuMatchChangeMods             PacketType = 51
	OsuMatchLoadComplete           PacketType = 52
	BanchoMatchAllPlayersLoaded    PacketType = 53
	OsuMatchNoBeatmap              PacketType = 54
	OsuMatchNotReady               PacketType = 55
	OsuMatchFailed                 PacketType = 56
	BanchoMatchPlayerFailed        PacketType = 57
	BanchoMatchComplete            PacketType = 58
	OsuMatchHasBeatmap             PacketType = 59
	OsuMatchSkipRequest            PacketType = 60
	BanchoMatchSkip                PacketType = 61
	BanchoUnauthorized             PacketType = 62
	OsuChannelJoin                 PacketType = 63
	BanchoChannelJoinSuccess       PacketType = 64
	BanchoChannelAvailable         PacketType = 65
	BanchoChannelRevoked           PacketType = 66
	BanchoChannelAvailableAutojoin PacketType = 67
	OsuBeatmapInfoRequest          PacketType = 68
	BanchoBeatmapInfoReply         PacketType = 69
	OsuMatchTransferHost           PacketType = 70
	BanchoLoginPermissions         PacketType = 71
	BanchoFriendsList              PacketType = 72
	OsuFriendsAdd                  PacketType = 73
	OsuFriendsRemove               PacketType = 74
	BanchoProtocolNegotiation      PacketType = 75
	BanchoTitleUpdate              PacketType = 76
	OsuMatchChangeTeam             PacketType = 77
	OsuChannelLeave                PacketType = 78
	OsuReceiveUpdates              PacketType = 79
	BanchoMonitor                  PacketType = 80
	BanchoMatchPlayerSkipped       PacketType = 81
	OsuSetIrcAwayMessage           PacketType = 82
	BanchoUserPresence             PacketType = 83
	OsuUserStatsRequest            PacketType = 85
	BanchoRestart                  PacketType = 86
	OsuInvite                      PacketType = 87
	BanchoInvite                   PacketType = 88
	BanchoChannelInfoComplete      PacketType = 89
	OsuMatchChangePassword         PacketType = 90
	BanchoMatchChangePassword      PacketType = 91
	BanchoSilenceInfo              PacketType = 92
	OsuTournamentMatchInfo         PacketType = 93
	BanchoUserSilenced             PacketType = 94
	BanchoUserPresenceSingle       PacketType = 95
	BanchoUserPresenceBundle       PacketType = 96
	OsuPresenceRequest             PacketType = 97
	OsuPresenceRequestAll          PacketType = 98
	OsuChangeFriendOnlyDms         PacketType = 99
	BanchoUserDmsBlocked           PacketType = 100
	BanchoTargetIsSilenced         PacketType = 101
	BanchoVersionUpdateForced      PacketType = 102
	BanchoSwitchServer             PacketType = 103
	BanchoAccountRestricted        PacketType = 104
	BanchoRTX                      PacketType = 105
	BanchoMatchAbort               PacketType = 106
	BanchoSwitchTournamentServer   PacketType = 107
	OsuTournamentJoinMatchChannel  PacketType = 108
	OsuTournamentLeaveMatchChannel PacketType = 109

	// Packets that are unused today, but used in legacy clients
	BanchoIrcJoin         PacketType = 0xFFFF
	OsuMatchChangeBeatmap PacketType = 0xFFFE
)

// MaxSize returns the maximum size for this packet type
func (pt PacketType) MaxSize() int {
	// In some cases, the beatmap info request packet can get really large
	if pt == OsuBeatmapInfoRequest {
		return 1 << 18 // 2^18
	}
	return 1 << 14 // 2^14
}

// IsServerPacket returns true if this is a server packet (starts with "Bancho")
func (pt PacketType) IsServerPacket() bool {
	return strings.HasPrefix(pt.String(), "Bancho")
}

// IsClientPacket returns true if this is a client packet (starts with "Osu")
func (pt PacketType) IsClientPacket() bool {
	return strings.HasPrefix(pt.String(), "Osu")
}

// HandlerName converts the packet type name to handler function name
func (pt PacketType) HandlerName() string {
	name := pt.String()
	// Convert camelCase to snake_case manually
	result := ""
	for i, r := range name {
		if i > 0 && 'A' <= r && r <= 'Z' {
			result += "_"
		}
		result += string(r)
	}
	name = strings.ToLower(result)
	name = strings.Replace(name, "osu_", "read_", -1)
	name = strings.Replace(name, "bancho_", "write_", -1)
	return name
}

// String returns the string representation of the packet type
func (pt PacketType) String() string {
	switch pt {
	case OsuUserStatus:
		return "OsuUserStatus"
	case OsuMessage:
		return "OsuMessage"
	case OsuExit:
		return "OsuExit"
	case OsuStatusUpdateRequest:
		return "OsuStatusUpdateRequest"
	case OsuPong:
		return "OsuPong"
	case BanchoLoginReply:
		return "BanchoLoginReply"
	case BanchoCommandError:
		return "BanchoCommandError"
	case BanchoMessage:
		return "BanchoMessage"
	case BanchoPing:
		return "BanchoPing"
	case BanchoIrcChangeUsername:
		return "BanchoIrcChangeUsername"
	case BanchoIrcQuit:
		return "BanchoIrcQuit"
	case BanchoUserStats:
		return "BanchoUserStats"
	case BanchoUserQuit:
		return "BanchoUserQuit"
	case BanchoSpectatorJoined:
		return "BanchoSpectatorJoined"
	case BanchoSpectatorLeft:
		return "BanchoSpectatorLeft"
	case BanchoSpectateFrames:
		return "BanchoSpectateFrames"
	case OsuStartSpectating:
		return "OsuStartSpectating"
	case OsuStopSpectating:
		return "OsuStopSpectating"
	case OsuSpectateFrames:
		return "OsuSpectateFrames"
	case BanchoVersionUpdate:
		return "BanchoVersionUpdate"
	case OsuErrorReport:
		return "OsuErrorReport"
	case OsuCantSpectate:
		return "OsuCantSpectate"
	case BanchoSpectatorCantSpectate:
		return "BanchoSpectatorCantSpectate"
	case BanchoGetAttention:
		return "BanchoGetAttention"
	case BanchoAnnounce:
		return "BanchoAnnounce"
	case OsuPrivateMessage:
		return "OsuPrivateMessage"
	case BanchoMatchUpdate:
		return "BanchoMatchUpdate"
	case BanchoMatchNew:
		return "BanchoMatchNew"
	case BanchoMatchDisband:
		return "BanchoMatchDisband"
	case OsuLobbyPart:
		return "OsuLobbyPart"
	case OsuLobbyJoin:
		return "OsuLobbyJoin"
	case OsuMatchCreate:
		return "OsuMatchCreate"
	case OsuMatchJoin:
		return "OsuMatchJoin"
	case OsuMatchPart:
		return "OsuMatchPart"
	case BanchoLobbyJoin:
		return "BanchoLobbyJoin"
	case BanchoLobbyPart:
		return "BanchoLobbyPart"
	case BanchoMatchJoinSuccess:
		return "BanchoMatchJoinSuccess"
	case BanchoMatchJoinFail:
		return "BanchoMatchJoinFail"
	case OsuMatchChangeSlot:
		return "OsuMatchChangeSlot"
	case OsuMatchReady:
		return "OsuMatchReady"
	case OsuMatchLock:
		return "OsuMatchLock"
	case OsuMatchChangeSettings:
		return "OsuMatchChangeSettings"
	case BanchoFellowSpectatorJoined:
		return "BanchoFellowSpectatorJoined"
	case BanchoFellowSpectatorLeft:
		return "BanchoFellowSpectatorLeft"
	case OsuMatchStart:
		return "OsuMatchStart"
	case BanchoMatchStart:
		return "BanchoMatchStart"
	case OsuMatchScoreUpdate:
		return "OsuMatchScoreUpdate"
	case BanchoMatchScoreUpdate:
		return "BanchoMatchScoreUpdate"
	case OsuMatchComplete:
		return "OsuMatchComplete"
	case BanchoMatchTransferHost:
		return "BanchoMatchTransferHost"
	case OsuMatchChangeMods:
		return "OsuMatchChangeMods"
	case OsuMatchLoadComplete:
		return "OsuMatchLoadComplete"
	case BanchoMatchAllPlayersLoaded:
		return "BanchoMatchAllPlayersLoaded"
	case OsuMatchNoBeatmap:
		return "OsuMatchNoBeatmap"
	case OsuMatchNotReady:
		return "OsuMatchNotReady"
	case OsuMatchFailed:
		return "OsuMatchFailed"
	case BanchoMatchPlayerFailed:
		return "BanchoMatchPlayerFailed"
	case BanchoMatchComplete:
		return "BanchoMatchComplete"
	case OsuMatchHasBeatmap:
		return "OsuMatchHasBeatmap"
	case OsuMatchSkipRequest:
		return "OsuMatchSkipRequest"
	case BanchoMatchSkip:
		return "BanchoMatchSkip"
	case BanchoUnauthorized:
		return "BanchoUnauthorized"
	case OsuChannelJoin:
		return "OsuChannelJoin"
	case BanchoChannelJoinSuccess:
		return "BanchoChannelJoinSuccess"
	case BanchoChannelAvailable:
		return "BanchoChannelAvailable"
	case BanchoChannelRevoked:
		return "BanchoChannelRevoked"
	case BanchoChannelAvailableAutojoin:
		return "BanchoChannelAvailableAutojoin"
	case OsuBeatmapInfoRequest:
		return "OsuBeatmapInfoRequest"
	case BanchoBeatmapInfoReply:
		return "BanchoBeatmapInfoReply"
	case OsuMatchTransferHost:
		return "OsuMatchTransferHost"
	case BanchoLoginPermissions:
		return "BanchoLoginPermissions"
	case BanchoFriendsList:
		return "BanchoFriendsList"
	case OsuFriendsAdd:
		return "OsuFriendsAdd"
	case OsuFriendsRemove:
		return "OsuFriendsRemove"
	case BanchoProtocolNegotiation:
		return "BanchoProtocolNegotiation"
	case BanchoTitleUpdate:
		return "BanchoTitleUpdate"
	case OsuMatchChangeTeam:
		return "OsuMatchChangeTeam"
	case OsuChannelLeave:
		return "OsuChannelLeave"
	case OsuReceiveUpdates:
		return "OsuReceiveUpdates"
	case BanchoMonitor:
		return "BanchoMonitor"
	case BanchoMatchPlayerSkipped:
		return "BanchoMatchPlayerSkipped"
	case OsuSetIrcAwayMessage:
		return "OsuSetIrcAwayMessage"
	case BanchoUserPresence:
		return "BanchoUserPresence"
	case OsuUserStatsRequest:
		return "OsuUserStatsRequest"
	case BanchoRestart:
		return "BanchoRestart"
	case OsuInvite:
		return "OsuInvite"
	case BanchoInvite:
		return "BanchoInvite"
	case BanchoChannelInfoComplete:
		return "BanchoChannelInfoComplete"
	case OsuMatchChangePassword:
		return "OsuMatchChangePassword"
	case BanchoMatchChangePassword:
		return "BanchoMatchChangePassword"
	case BanchoSilenceInfo:
		return "BanchoSilenceInfo"
	case OsuTournamentMatchInfo:
		return "OsuTournamentMatchInfo"
	case BanchoUserSilenced:
		return "BanchoUserSilenced"
	case BanchoUserPresenceSingle:
		return "BanchoUserPresenceSingle"
	case BanchoUserPresenceBundle:
		return "BanchoUserPresenceBundle"
	case OsuPresenceRequest:
		return "OsuPresenceRequest"
	case OsuPresenceRequestAll:
		return "OsuPresenceRequestAll"
	case OsuChangeFriendOnlyDms:
		return "OsuChangeFriendOnlyDms"
	case BanchoUserDmsBlocked:
		return "BanchoUserDmsBlocked"
	case BanchoTargetIsSilenced:
		return "BanchoTargetIsSilenced"
	case BanchoVersionUpdateForced:
		return "BanchoVersionUpdateForced"
	case BanchoSwitchServer:
		return "BanchoSwitchServer"
	case BanchoAccountRestricted:
		return "BanchoAccountRestricted"
	case BanchoRTX:
		return "BanchoRTX"
	case BanchoMatchAbort:
		return "BanchoMatchAbort"
	case BanchoSwitchTournamentServer:
		return "BanchoSwitchTournamentServer"
	case OsuTournamentJoinMatchChannel:
		return "OsuTournamentJoinMatchChannel"
	case OsuTournamentLeaveMatchChannel:
		return "OsuTournamentLeaveMatchChannel"
	case BanchoIrcJoin:
		return "BanchoIrcJoin"
	case OsuMatchChangeBeatmap:
		return "OsuMatchChangeBeatmap"
	default:
		return "Unknown"
	}
}

// Status represents the user status
type Status int

const (
	StatusIdle         Status = 0
	StatusAfk          Status = 1
	StatusPlaying      Status = 2
	StatusEditing      Status = 3
	StatusModding      Status = 4
	StatusMultiplayer  Status = 5
	StatusWatching     Status = 6
	StatusUnknown      Status = 7
	StatusTesting      Status = 8
	StatusSubmitting   Status = 9
	StatusPaused       Status = 10
	StatusLobby        Status = 11
	StatusMultiplaying Status = 12
	StatusOsuDirect    Status = 13

	// Unused in later versions, but required for compatibility
	StatusStatsUpdate Status = 10
)

// Mode represents the game mode
type Mode int

const (
	ModeOsu          Mode = 0
	ModeTaiko        Mode = 1
	ModeCatchTheBeat Mode = 2
	ModeMania        Mode = 3
)

// FromAlias converts a string alias to Mode
func (m Mode) FromAlias(input string) Mode {
	mapping := map[string]Mode{
		"std":    ModeOsu,
		"osu":    ModeOsu,
		"taiko":  ModeTaiko,
		"fruits": ModeCatchTheBeat,
		"ctb":    ModeCatchTheBeat,
		"catch":  ModeCatchTheBeat,
		"mania":  ModeMania,
	}

	if mode, exists := mapping[input]; exists {
		return mode
	}
	return ModeOsu // default
}

// Formatted returns the formatted string representation
func (m Mode) Formatted() string {
	switch m {
	case ModeOsu:
		return "osu!"
	case ModeTaiko:
		return "Taiko"
	case ModeCatchTheBeat:
		return "CatchTheBeat"
	case ModeMania:
		return "osu!mania"
	default:
		return "osu!"
	}
}

// Alias returns the short alias
func (m Mode) Alias() string {
	switch m {
	case ModeOsu:
		return "osu"
	case ModeTaiko:
		return "taiko"
	case ModeCatchTheBeat:
		return "fruits"
	case ModeMania:
		return "mania"
	default:
		return "osu"
	}
}

// LoginError represents login errors
type LoginError int

const (
	InvalidLogin          LoginError = -1
	InvalidVersion        LoginError = -2
	UserBanned            LoginError = -3
	UserInactive          LoginError = -4
	ServerError           LoginError = -5
	UnauthorizedTestBuild LoginError = -6
	PasswordReset         LoginError = -7
	VerificationRequired  LoginError = -8
)

// Permissions represents user permissions (bitmask)
type Permissions int

const (
	NoPermissions Permissions = 0
	Regular       Permissions = 1 << 0
	BAT           Permissions = 1 << 1
	Supporter     Permissions = 1 << 2
	Friend        Permissions = 1 << 3
	Peppy         Permissions = 1 << 4
	TournamentMod Permissions = 1 << 5
)

// QuitState represents quit state
type QuitState int

const (
	Gone         QuitState = 0
	OsuRemaining QuitState = 1
	IrcRemaining QuitState = 2
)

// AvatarExtension represents avatar file extension
type AvatarExtension int

const (
	EmptyExtension AvatarExtension = 0
	PngExtension   AvatarExtension = 1
	JpgExtension   AvatarExtension = 2
)

// PresenceFilter represents presence filter
type PresenceFilter int

const (
	NoPlayers PresenceFilter = 0
	All       PresenceFilter = 1
	Friends   PresenceFilter = 2
)

// Completeness represents data completeness
type Completeness int

const (
	StatusOnly Completeness = 0
	Statistics Completeness = 1
	Full       Completeness = 2
)

// ReplayAction represents replay actions
type ReplayAction int

const (
	StandardAction      ReplayAction = 0
	NewSong            ReplayAction = 1
	Skip               ReplayAction = 2
	Completion         ReplayAction = 3
	Fail               ReplayAction = 4
	Pause              ReplayAction = 5
	Unpause            ReplayAction = 6
	SongSelect         ReplayAction = 7
	WatchingOther      ReplayAction = 8
)

// ButtonState represents button state (bitmask)
type ButtonState int

const (
	NoButton ButtonState = 0
	Left1    ButtonState = 1 << 0
	Right1   ButtonState = 1 << 1
	Left2    ButtonState = 1 << 2
	Right2   ButtonState = 1 << 3
	Smoke    ButtonState = 1 << 4
)

// Rank represents performance rank
type Rank int

const (
	XH Rank = 0
	SH Rank = 1
	X  Rank = 2
	S  Rank = 3
	A  Rank = 4
	B  Rank = 5
	C  Rank = 6
	D  Rank = 7
	F  Rank = 8
)

// Mods represents game mods (bitmask)
type Mods int

const (
	NoMod         Mods = 0
	NoFail        Mods = 1 << 0
	Easy          Mods = 1 << 1
	TouchDevice   Mods = 1 << 2
	Hidden        Mods = 1 << 3
	HardRock      Mods = 1 << 4
	SuddenDeath   Mods = 1 << 5
	DoubleTime    Mods = 1 << 6
	Relax         Mods = 1 << 7
	HalfTime      Mods = 1 << 8
	Nightcore     Mods = 1 << 9
	Flashlight    Mods = 1 << 10
	Autoplay      Mods = 1 << 11
	SpunOut       Mods = 1 << 12
	Autopilot     Mods = 1 << 13
	Perfect       Mods = 1 << 14
	Key4          Mods = 1 << 15
	Key5          Mods = 1 << 16
	Key6          Mods = 1 << 17
	Key7          Mods = 1 << 18
	Key8          Mods = 1 << 19
	FadeIn        Mods = 1 << 20
	Random        Mods = 1 << 21
	Cinema        Mods = 1 << 22
	Target        Mods = 1 << 23
	Key9          Mods = 1 << 24
	KeyCoop       Mods = 1 << 25
	Key1          Mods = 1 << 26
	Key3          Mods = 1 << 27
	Key2          Mods = 1 << 28
	ScoreV2       Mods = 1 << 29
	Mirror        Mods = 1 << 30
)

// MatchType represents match type
type MatchType int

const (
	Standard   MatchType = 0
	Powerplay  MatchType = 1
	Tournament MatchType = 2
)

// ScoringType represents scoring type
type ScoringType int

const (
	Score       ScoringType = 0
	Accuracy    ScoringType = 1
	Combo       ScoringType = 2
	ScoreV2Type ScoringType = 3
)

// TeamType represents team type
type TeamType int

const (
	HeadToHead TeamType = 0
	TagCoop    TeamType = 1
	TeamVs     TeamType = 2
	TagTeamVs  TeamType = 3
)

// SlotStatus represents slot status
type SlotStatus int

const (
	Open       SlotStatus = 1
	Locked     SlotStatus = 2
	NotReady   SlotStatus = 4
	Ready      SlotStatus = 8
	NoMap      SlotStatus = 16
	Playing    SlotStatus = 32
	Complete   SlotStatus = 64
	Quit       SlotStatus = 128
)

// HasPlayer returns true if the slot has a player
func (ss SlotStatus) HasPlayer() bool {
	return ss&(NotReady|Ready|NoMap|Playing|Complete) != 0
}

// SlotTeam represents slot team
type SlotTeam int

const (
	Neutral SlotTeam = 0
	Blue    SlotTeam = 1
	Red     SlotTeam = 2
)

// Opposite returns the opposite team
func (st SlotTeam) Opposite() SlotTeam {
	if st == Red {
		return Blue
	}
	return Red
}

// RankedStatus represents ranked status
type RankedStatus int

const (
	NotSubmitted RankedStatus = -1
	Pending      RankedStatus = 0
	Ranked       RankedStatus = 1
	Approved     RankedStatus = 2
	Qualified    RankedStatus = 3
	Loved        RankedStatus = 4
)