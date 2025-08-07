
from functools import cached_property
from enum import IntFlag, IntEnum
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
    "RankedStatus",
    "InactiveAccountMessage",
    "Countries",
    "CountryNames",
    "CountryAcronyms",
    "ChatLinkModern",
    "ChatLinkLegacy"
]

# Regex to convert camelCase to snake_case
# Example: "OsuSendUserStatus" -> "osu_send_user_status"
CaseConvertPattern = compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

# Chat link regex patterns:
# Modern: [http://example.com Example]
# Legacy: (Example)[http://example.com]
ChatLinkModern = compile(r"\[((?:https?:\/\/)[^\s\]]+)\s+(.+?)\]")
ChatLinkLegacy = compile(r"\[([^\]]+)\]\((https?:\/\/[^)]+)\)")

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
    OsuChangeFriendOnlyDms         = 99
    BanchoUserDmsBlocked           = 100
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
    def max_size(self) -> int:
        # In some cases, the beatmap info request packet can get really large
        return 2**14 if self != PacketType.OsuBeatmapInfoRequest else 2**18

    @cached_property
    def is_server_packet(self) -> bool:
        return self.name.startswith("Bancho")

    @cached_property
    def is_client_packet(self) -> bool:
        return self.name.startswith("Osu")

    @cached_property
    def handler_name(self) -> str:
        name = CaseConvertPattern.sub("_", self.name).lower()
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
    Osu          = 0
    Taiko        = 1
    CatchTheBeat = 2
    OsuMania     = 3

    @classmethod
    def from_alias(cls, input: str):
        mapping = {
            'std': Mode.Osu,
            'osu': Mode.Osu,
            'taiko': Mode.Taiko,
            'fruits': Mode.CatchTheBeat,
            'ctb': Mode.CatchTheBeat,
            'catch': Mode.CatchTheBeat,
            'mania': Mode.OsuMania
        }

        if input not in mapping:
            return

        return mapping[input]

    @property
    def formatted(self) -> str:
        return {
            Mode.Osu: 'osu!',
            Mode.Taiko: 'Taiko',
            Mode.CatchTheBeat: 'CatchTheBeat',
            Mode.OsuMania: 'osu!mania'
        }[self]

    @property
    def alias(self) -> str:
        return {
            Mode.Osu: 'osu',
            Mode.Taiko: 'taiko',
            Mode.CatchTheBeat: 'fruits',
            Mode.OsuMania: 'mania'
        }[self]

class LoginError(IntEnum):
    InvalidLogin          = -1
    InvalidVersion        = -2
    UserBanned            = -3
    UserInactive          = -4
    ServerError           = -5
    UnauthorizedTestBuild = -6
    PasswordReset         = -7
    VerificationRequired  = -8

class Permissions(IntFlag):
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

class ButtonState(IntFlag):
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

class Mods(IntFlag):
    NoMod       = 0
    NoFail      = 1 << 0
    Easy        = 1 << 1
    NoVideo     = 1 << 2 # replaced by "Touchscreen" in later versions
    Hidden      = 1 << 3
    HardRock    = 1 << 4
    SuddenDeath = 1 << 5
    DoubleTime  = 1 << 6
    Relax       = 1 << 7
    HalfTime    = 1 << 8
    Nightcore   = 1 << 9 # used as "Taiko" mod in older versions
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

    KeyMod = Key1 | Key2 | Key3 | Key4 | Key5 | Key6 | Key7 | Key8 | Key9 | KeyCoop
    FreeModAllowed = NoFail | Easy | Hidden | HardRock | SuddenDeath | Flashlight | FadeIn | Relax | Autopilot | SpunOut | KeyMod
    SpeedMods = DoubleTime | HalfTime | Nightcore

    @property
    def members(self) -> list:
        return [flag for flag in Mods if self & flag]

    @property
    def short(self) -> str:
        if not self:
            return "NM"

        return "".join(
            [ModAcronyms.get(flag, "") for flag in self.members]
        )
    
    @classmethod
    def from_string(cls, acronym_string: str) -> "Mods":
        mods = Mods.NoMod

        if not acronym_string:
            return mods

        # Parse mods into multiple acronyms
        # .e.g. "HDHR" -> ["HR", "HD"]
        parsed_mods = [
            acronym_string[idx : idx + 2].upper()
            for idx in range(0, len(acronym_string), 2)
        ]

        for acronym in parsed_mods:
            mod = ModAcronymsFromString.get(acronym)

            if mod:
                mods |= mod

        return mods

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
    TagTeamVs  = 3

class SlotStatus(IntFlag):
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

    @property
    def opposite(self) -> "SlotTeam":
        return SlotTeam.Red if self != SlotTeam.Red else SlotTeam.Blue

class RankedStatus(IntEnum):
    NotSubmitted = -1
    Pending      = 0
    Ranked       = 1
    Approved     = 2
    Qualified    = 3
    Loved        = 4

InactiveAccountMessage = (
    "Your account is not yet activated. "
    "Please check your email for activation instructions!"
)

ModAcronyms = {
    Mods.NoMod: "NM",
    Mods.NoFail: "NF",
    Mods.Easy: "EZ",
    Mods.NoVideo: "NV",
    Mods.Hidden: "HD",
    Mods.HardRock: "HR",
    Mods.SuddenDeath: "SD",
    Mods.DoubleTime: "DT",
    Mods.Relax: "RX",
    Mods.HalfTime: "HT",
    Mods.Nightcore: "NC",
    Mods.Flashlight: "FL",
    Mods.Autoplay: "AT",
    Mods.SpunOut: "SO",
    Mods.Autopilot: "AP",
    Mods.Perfect: "PF",
    Mods.Key4: "K4",
    Mods.Key5: "K5",
    Mods.Key6: "K6",
    Mods.Key7: "K7",
    Mods.Key8: "K8",
    Mods.FadeIn: "FI",
    Mods.Random: "RD",
    Mods.Cinema: "CN",
    Mods.Target: "TP",
    Mods.Key9: "K9",
    Mods.KeyCoop: "CP",
    Mods.Key1: "K1",
    Mods.Key3: "K3",
    Mods.Key2: "K2",
    Mods.ScoreV2: "V2",
    Mods.Mirror: "MR",
    Mods.SpeedMods: "",
    Mods.KeyMod: "",
    Mods.FreeModAllowed: ""
}

ModAcronymsFromString = {
    "NM": Mods.NoMod,
    "NF": Mods.NoFail,
    "EZ": Mods.Easy,
    "NV": Mods.NoVideo,
    "HD": Mods.Hidden,
    "HR": Mods.HardRock,
    "SD": Mods.SuddenDeath,
    "DT": Mods.DoubleTime,
    "RX": Mods.Relax,
    "HT": Mods.HalfTime,
    "NC": Mods.Nightcore,
    "FL": Mods.Flashlight,
    "AT": Mods.Autoplay,
    "SO": Mods.SpunOut,
    "AP": Mods.Autopilot,
    "PF": Mods.Perfect,
    "K4": Mods.Key4,
    "K5": Mods.Key5,
    "K6": Mods.Key6,
    "K7": Mods.Key7,
    "K8": Mods.Key8,
    "FI": Mods.FadeIn,
    "RD": Mods.Random,
    "CN": Mods.Cinema,
    "TP": Mods.Target,
    "K9": Mods.Key9,
    "CP": Mods.KeyCoop,
    "K1": Mods.Key1,
    "K3": Mods.Key3,
    "K2": Mods.Key2,
    "V2": Mods.ScoreV2,
    "MR": Mods.Mirror
}

Countries = {
    "XX": "Unknown",
    "OC": "Oceania",
    "EU": "Europe",
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua and Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AN": "Netherlands Antilles",
    "AO": "Angola",
    "AQ": "Antarctica",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BN": "Brunei Darussalam",
    "BO": "Bolivia",
    "BR": "Brazil",
    "BS": "The Bahamas",
    "BT": "Bhutan",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CD": "Democratic Republic of the Congo",
    "CF": "Central African Republic",
    "CG": "Republic of the Congo",
    "CH": "Switzerland",
    "CI": "Côte d'Ivoire",
    "CK": "Cook Islands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CV": "Cape Verde",
    "CX": "Christmas Island",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands (Malvinas)",
    "FM": "Micronesia, Federated States of Micronesia",
    "FO": "Faroe Islands",
    "FR": "France",
    "FX": "France, Metropolitan",
    "GA": "Gabon",
    "GB": "United Kingdom",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard Island and McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Iran, Islamic Republic of Iran",
    "IS": "Iceland",
    "IT": "Italy",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "Saint Kitts and Nevis",
    "KP": "Korea, Democratic People's Republic of Korea",
    "KR": "Korea, Republic of Korea",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Lao People's Democratic Republic",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libyan Arab Jamahiriya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova, Republic of Moldova",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "MK": "Macedonia, the Former Yugoslav Republic of Macedonia",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "Saint Pierre and Miquelon",
    "PN": "Pitcairn",
    "PR": "Puerto Rico",
    "PS": "Palestinian Territory, Occupied",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "Saint Helena, Ascension and Tristan da Cunha",
    "SI": "Slovenia",
    "SJ": "Svalbard and Jan Mayen",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "ST": "Sao Tome and Principe",
    "SV": "El Salvador",
    "SY": "Syrian Arab Republic",
    "SZ": "Eswatini",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TL": "Timor-Leste",
    "TR": "Turkey",
    "TT": "Trinidad and Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan",
    "TZ": "Tanzania",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UM": "United States Minor Outlying Islands",
    "US": "United States",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Holy See",
    "VC": "Saint Vincent",
    "VE": "Venezuela",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "VN": "Vietnam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "YE": "Yemen",
    "YT": "Mayotte",
    "RS": "Serbia",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ME": "Montenegro",
    "ZW": "Zimbabwe",
    "A1": "Unknown",
    "A2": "Satellite Provider",
    "O1": "Other",
    "AX": "Aland Islands",
    "GG": "Guernsey",
    "IM": "Isle of Man",
    "JE": "Jersey",
    "BL": "St. Barthelemy",
    "MF": "Saint Martin",
}

CountryNames = list(Countries.values())
CountryAcronyms = list(Countries.keys())
