package types

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/Lekuruu/chio.py/chio-go/constants"
)

// Countries slice for country lookups (would be populated from Python constants)
var CountryNames = []string{
	"Unknown", "Satellite Provider", "Andorra", "United Arab Emirates", "Afghanistan",
	// ... would include all countries from Python version
}

var CountryAcronyms = []string{
	"XX", "SP", "AD", "AE", "AF",
	// ... would include all country codes from Python version
}

// UserPresence represents user presence information
type UserPresence struct {
	IsIRC        bool                  `json:"is_irc"`
	Timezone     int                   `json:"timezone"`
	CountryIndex int                   `json:"country_index"`
	Permissions  constants.Permissions `json:"permissions"`
	Longitude    float64               `json:"longitude"`
	Latitude     float64               `json:"latitude"`
	City         string                `json:"city"`
}

// CountryName returns the country name
func (up *UserPresence) CountryName() string {
	if up.CountryIndex >= 0 && up.CountryIndex < len(CountryNames) {
		return CountryNames[up.CountryIndex]
	}
	return "Unknown"
}

// CountryAcronym returns the country acronym
func (up *UserPresence) CountryAcronym() string {
	if up.CountryIndex >= 0 && up.CountryIndex < len(CountryAcronyms) {
		return CountryAcronyms[up.CountryIndex]
	}
	return "XX"
}

// CountryString returns formatted country string with optional city
func (up *UserPresence) CountryString() string {
	countryName := up.CountryName()
	if up.City == "" {
		return countryName
	}
	return fmt.Sprintf("%s / %s", countryName, up.City)
}

// UserStats represents user statistics
type UserStats struct {
	Rank      int     `json:"rank"`
	RScore    int     `json:"rscore"`
	TScore    int     `json:"tscore"`
	Accuracy  float32 `json:"accuracy"`
	PlayCount int     `json:"playcount"`
	PP        int     `json:"pp"`
}

// UserStatus represents user status
type UserStatus struct {
	Action          constants.Status `json:"action"`
	Text            string           `json:"text"`
	Mods            constants.Mods   `json:"mods"`
	Mode            constants.Mode   `json:"mode"`
	BeatmapChecksum string           `json:"beatmap_checksum"`
	BeatmapID       int              `json:"beatmap_id"`
	UpdateStats     bool             `json:"update_stats"`
}

// Reset resets the user status to default values
func (us *UserStatus) Reset() {
	us.Action = constants.StatusIdle
	us.Text = ""
	us.Mods = constants.NoMod
	us.Mode = constants.ModeOsu
	us.BeatmapChecksum = ""
	us.BeatmapID = -1
	us.UpdateStats = false
}

// UserInfo represents complete user information
type UserInfo struct {
	ID       int          `json:"id"`
	Name     string       `json:"name"`
	Presence UserPresence `json:"presence"`
	Status   UserStatus   `json:"status"`
	Stats    UserStats    `json:"stats"`
}

// AvatarFilename returns the avatar filename for this user
func (ui *UserInfo) AvatarFilename() string {
	return fmt.Sprintf("%d_000.png", ui.ID)
}

// UserQuit represents user quit information
type UserQuit struct {
	Info  UserInfo            `json:"info"`
	State constants.QuitState `json:"state"`
}

// Message represents a chat message
type Message struct {
	Sender   string `json:"sender"`
	Content  string `json:"content"`
	Target   string `json:"target"`
	SenderID int    `json:"sender_id"`
}

// Chat link regex patterns
var chatLinkModern = regexp.MustCompile(`\[((?:https?:\/\/)[^\s\]]+)\s+((?:[^\[\]]|\[[^\[\]]*\])*)\]`)

// ContentMarkdownFormatted returns the message content in the legacy, markdown-ish format
func (m *Message) ContentMarkdownFormatted() string {
	return chatLinkModern.ReplaceAllString(m.Content, "($2)[$1]")
}

// IsDirectMessage checks if the message is a direct message
func (m *Message) IsDirectMessage() bool {
	return !strings.HasPrefix(m.Target, "#")
}

// Channel represents a chat channel
type Channel struct {
	Name      string `json:"name"`
	Topic     string `json:"topic"`
	Owner     string `json:"owner"`
	UserCount int    `json:"user_count"`
}

// BeatmapInfo represents beatmap information
type BeatmapInfo struct {
	Index        int                    `json:"index"`
	BeatmapID    int                    `json:"beatmap_id"`
	BeatmapsetID int                    `json:"beatmapset_id"`
	ThreadID     int                    `json:"thread_id"`
	RankedStatus constants.RankedStatus `json:"ranked_status"`
	Checksum     string                 `json:"checksum"`
	OsuRank      constants.Rank         `json:"osu_rank"`
	TaikoRank    constants.Rank         `json:"taiko_rank"`
	FruitsRank   constants.Rank         `json:"fruits_rank"`
	ManiaRank    constants.Rank         `json:"mania_rank"`
}

// IsRanked returns true if the beatmap is ranked or approved
func (bi *BeatmapInfo) IsRanked() bool {
	return bi.RankedStatus == constants.Ranked || bi.RankedStatus == constants.Approved
}

// BeatmapInfoReply represents a reply with beatmap information
type BeatmapInfoReply struct {
	Beatmaps []BeatmapInfo `json:"beatmaps"`
}

// BeatmapInfoRequest represents a request for beatmap information
type BeatmapInfoRequest struct {
	Filenames []string `json:"filenames"`
	IDs       []int    `json:"ids"`
}

// ReplayFrame represents a single replay frame
type ReplayFrame struct {
	ButtonState constants.ButtonState `json:"button_state"`
	TaikoState  int                   `json:"taiko_state"`
	X           float32               `json:"x"`
	Y           float32               `json:"y"`
	Time        int                   `json:"time"`
}

// ScoreFrame represents a score frame
type ScoreFrame struct {
	Time         int     `json:"time"`
	ID           int     `json:"id"`
	Count300     int     `json:"count_300"`
	Count100     int     `json:"count_100"`
	Count50      int     `json:"count_50"`
	CountGeki    int     `json:"count_geki"`
	CountKatu    int     `json:"count_katu"`
	CountMiss    int     `json:"count_miss"`
	TotalScore   int     `json:"total_score"`
	MaxCombo     int     `json:"max_combo"`
	CurrentCombo int     `json:"current_combo"`
	Perfect      bool    `json:"perfect"`
	CurrentHP    int     `json:"current_hp"`
	TagByte      int     `json:"tag_byte"`
	ScoreV2      bool    `json:"score_v2"`
	ComboPortion float64 `json:"combo_portion"`
	BonusPortion float64 `json:"bonus_portion"`
}

// ReplayFrameBundle represents a bundle of replay frames
type ReplayFrameBundle struct {
	Frames     []ReplayFrame          `json:"frames"`
	Action     constants.ReplayAction `json:"action"`
	ScoreFrame *ScoreFrame            `json:"score_frame,omitempty"`
	Extra      int                    `json:"extra"`
	RawData    []byte                 `json:"raw_data,omitempty"`
}

// MatchSlot represents a multiplayer match slot
type MatchSlot struct {
	Status constants.SlotStatus `json:"status"`
	Team   constants.SlotTeam   `json:"team"`
	UserID int                  `json:"user_id"`
	Mods   constants.Mods       `json:"mods"`
}

// HasPlayer returns true if the slot has a player
func (ms *MatchSlot) HasPlayer() bool {
	return ms.Status.HasPlayer()
}

// Match represents a multiplayer match
type Match struct {
	ID              int                   `json:"id"`
	InProgress      bool                  `json:"in_progress"`
	Type            constants.MatchType   `json:"type"`
	Mods            constants.Mods        `json:"mods"`
	Name            string                `json:"name"`
	Password        string                `json:"password"`
	BeatmapText     string                `json:"beatmap_text"`
	BeatmapID       int                   `json:"beatmap_id"`
	BeatmapChecksum string                `json:"beatmap_checksum"`
	Slots           []MatchSlot           `json:"slots"`
	HostID          int                   `json:"host_id"`
	Mode            constants.Mode        `json:"mode"`
	ScoringType     constants.ScoringType `json:"scoring_type"`
	TeamType        constants.TeamType    `json:"team_type"`
	Freemod         bool                  `json:"freemod"`
	Seed            int                   `json:"seed"`
}

// MatchJoin represents a match join request
type MatchJoin struct {
	MatchID  int    `json:"match_id"`
	Password string `json:"password"`
}

// TitleUpdate represents a title update
type TitleUpdate struct {
	ImageURL    string `json:"image_url"`
	RedirectURL string `json:"redirect_url"`
}
