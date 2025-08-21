package clients

import (
	"context"
	"fmt"

	"github.com/Lekuruu/chio.py/chio-go/constants"
	"github.com/Lekuruu/chio.py/chio-go/io"
	"github.com/Lekuruu/chio.py/chio-go/types"
)

// B282Client represents the b282 client implementation
// b282 is the initial implementation of the bancho protocol.
// Every following version will be based on it.
type B282Client struct {
	version               int
	slotSize              int
	headerSize            int
	protocolVersion       int
	disableCompression    bool
	requiresStatusUpdates bool
	autojoinChannels      []string
}

// NewB282Client creates a new B282 client
func NewB282Client() *B282Client {
	return &B282Client{
		version:               282,
		slotSize:              8,
		headerSize:            6,
		protocolVersion:       0,
		disableCompression:    false,
		requiresStatusUpdates: true,
		autojoinChannels:      []string{"#osu", "#announce"},
	}
}

// Version returns the client version
func (c *B282Client) Version() int {
	return c.version
}

// SlotSize returns the slot size
func (c *B282Client) SlotSize() int {
	return c.slotSize
}

// HeaderSize returns the header size
func (c *B282Client) HeaderSize() int {
	return c.headerSize
}

// ProtocolVersion returns the protocol version
func (c *B282Client) ProtocolVersion() int {
	return c.protocolVersion
}

// DisableCompression returns whether compression is disabled
func (c *B282Client) DisableCompression() bool {
	return c.disableCompression
}

// RequiresStatusUpdates returns whether status updates are required
func (c *B282Client) RequiresStatusUpdates() bool {
	return c.requiresStatusUpdates
}

// AutojoinChannels returns the channels to auto-join
func (c *B282Client) AutojoinChannels() []string {
	return c.autojoinChannels
}

// ReadPacket reads a packet from the stream
func (c *B282Client) ReadPacket(stream io.Stream) (constants.PacketType, interface{}, error) {
	// Read packet ID (16-bit)
	packetID, err := io.ReadU16(stream)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read packet ID: %v", err)
	}

	packet := constants.PacketType(packetID)

	// Validate it's a client packet
	if !packet.IsClientPacket() {
		return 0, nil, fmt.Errorf("packet '%s' is not a client packet", packet.String())
	}

	// Read packet length (32-bit)
	packetLength, err := io.ReadU32(stream)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read packet length: %v", err)
	}

	// Validate packet size
	if int(packetLength) >= packet.MaxSize() {
		return 0, nil, fmt.Errorf("packet '%s' with length '%d' is too large", packet.String(), packetLength)
	}

	// Read and decompress packet data
	packetData, err := io.ReadGzip(stream, int(packetLength))
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read packet data: %v", err)
	}

	// Create a memory stream for the packet data
	dataStream := io.NewMemoryStream(packetData)

	// Handle the packet based on its type
	data, err := c.handleReadPacket(packet, dataStream)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to handle packet '%s': %v", packet.String(), err)
	}

	return packet, data, nil
}

// WritePacket writes a packet to the stream
func (c *B282Client) WritePacket(stream io.Stream, packet constants.PacketType, args ...interface{}) error {
	// Validate it's a server packet
	if !packet.IsServerPacket() {
		return fmt.Errorf("packet '%s' is not a server packet", packet.String())
	}

	// Handle the packet based on its type and get the data to write
	packets, err := c.handleWritePacket(packet, args...)
	if err != nil {
		return fmt.Errorf("failed to handle packet '%s': %v", packet.String(), err)
	}

	// Write each packet
	for _, packetData := range packets {
		outputStream := io.NewMemoryStream(nil)

		// Compress the packet data
		err := io.WriteGzip(outputStream, packetData.Data)
		if err != nil {
			return fmt.Errorf("failed to compress packet data: %v", err)
		}

		// Write packet header (ID + length) and compressed data
		err = io.WriteU16(stream, int(packetData.Type))
		if err != nil {
			return fmt.Errorf("failed to write packet ID: %v", err)
		}

		compressedData := outputStream.Data()
		err = io.WriteU32(stream, int64(len(compressedData)))
		if err != nil {
			return fmt.Errorf("failed to write packet length: %v", err)
		}

		err = stream.Write(compressedData)
		if err != nil {
			return fmt.Errorf("failed to write packet data: %v", err)
		}
	}

	return nil
}

// PacketData represents packet type and data
type PacketData struct {
	Type constants.PacketType
	Data []byte
}

// handleReadPacket handles reading different packet types
func (c *B282Client) handleReadPacket(packet constants.PacketType, stream io.Stream) (interface{}, error) {
	switch packet {
	case constants.OsuUserStatus:
		return c.readUserStatus(stream)
	case constants.OsuMessage:
		return c.readMessage(stream)
	case constants.OsuExit:
		return c.readExit(stream)
	case constants.OsuPong:
		return nil, nil // No data for pong
	default:
		return nil, fmt.Errorf("packet '%s' not implemented for reading", packet.String())
	}
}

// handleWritePacket handles writing different packet types
func (c *B282Client) handleWritePacket(packet constants.PacketType, args ...interface{}) ([]PacketData, error) {
	switch packet {
	case constants.BanchoLoginReply:
		return c.writeLoginReply(args...)
	case constants.BanchoMessage:
		return c.writeMessage(args...)
	case constants.BanchoPing:
		return c.writePing(args...)
	case constants.BanchoUserStats:
		return c.writeUserStats(args...)
	default:
		return nil, fmt.Errorf("packet '%s' not implemented for writing", packet.String())
	}
}

// Reader implementations

// readUserStatus reads user status
func (c *B282Client) readUserStatus(stream io.Stream) (*types.UserStatus, error) {
	status := &types.UserStatus{}

	action, err := io.ReadU8(stream)
	if err != nil {
		return nil, err
	}
	status.Action = c.convertInputStatus(constants.Status(action))

	if status.Action != constants.StatusUnknown {
		status.Text, err = io.ReadString(stream)
		if err != nil {
			return nil, err
		}

		status.BeatmapChecksum, err = io.ReadString(stream)
		if err != nil {
			return nil, err
		}

		mods, err := io.ReadU16(stream)
		if err != nil {
			return nil, err
		}
		status.Mods = constants.Mods(mods)
	}

	return status, nil
}

// readMessage reads a message
func (c *B282Client) readMessage(stream io.Stream) (*types.Message, error) {
	message := &types.Message{}

	var err error
	message.Sender, err = io.ReadString(stream)
	if err != nil {
		return nil, err
	}

	message.Content, err = io.ReadString(stream)
	if err != nil {
		return nil, err
	}

	message.Target, err = io.ReadString(stream)
	if err != nil {
		return nil, err
	}

	return message, nil
}

// readExit reads exit packet
func (c *B282Client) readExit(stream io.Stream) (bool, error) {
	return io.ReadBoolean(stream)
}

// Writer implementations

// writeLoginReply writes login reply
func (c *B282Client) writeLoginReply(args ...interface{}) ([]PacketData, error) {
	if len(args) == 0 {
		return nil, fmt.Errorf("login reply requires user ID argument")
	}

	// Handle both int (user ID) and LoginError
	stream := io.NewMemoryStream(nil)

	switch v := args[0].(type) {
	case int:
		err := io.WriteS32(stream, int64(v))
		if err != nil {
			return nil, err
		}
	case constants.LoginError:
		err := io.WriteS32(stream, int64(v))
		if err != nil {
			return nil, err
		}
	default:
		return nil, fmt.Errorf("invalid login reply argument type: %T", v)
	}

	return []PacketData{{
		Type: constants.BanchoLoginReply,
		Data: stream.Data(),
	}}, nil
}

// writeMessage writes a message
func (c *B282Client) writeMessage(args ...interface{}) ([]PacketData, error) {
	if len(args) == 0 {
		return nil, fmt.Errorf("message write requires message argument")
	}

	message, ok := args[0].(*types.Message)
	if !ok {
		return nil, fmt.Errorf("invalid message argument type: %T", args[0])
	}

	stream := io.NewMemoryStream(nil)

	err := io.WriteString(stream, message.Sender)
	if err != nil {
		return nil, err
	}

	err = io.WriteString(stream, message.Content)
	if err != nil {
		return nil, err
	}

	err = io.WriteString(stream, message.Target)
	if err != nil {
		return nil, err
	}

	err = io.WriteS32(stream, int64(message.SenderID))
	if err != nil {
		return nil, err
	}

	return []PacketData{{
		Type: constants.BanchoMessage,
		Data: stream.Data(),
	}}, nil
}

// writePing writes a ping packet
func (c *B282Client) writePing(args ...interface{}) ([]PacketData, error) {
	return []PacketData{{
		Type: constants.BanchoPing,
		Data: []byte{}, // Empty data for ping
	}}, nil
}

// writeUserStats writes user statistics
func (c *B282Client) writeUserStats(args ...interface{}) ([]PacketData, error) {
	if len(args) == 0 {
		return nil, fmt.Errorf("user stats write requires user info argument")
	}

	userInfo, ok := args[0].(*types.UserInfo)
	if !ok {
		return nil, fmt.Errorf("invalid user info argument type: %T", args[0])
	}

	stream := io.NewMemoryStream(nil)

	err := io.WriteS32(stream, int64(userInfo.ID))
	if err != nil {
		return nil, err
	}

	// Write status update
	statusData, err := c.writeStatusUpdate(&userInfo.Status)
	if err != nil {
		return nil, err
	}
	err = stream.Write(statusData)
	if err != nil {
		return nil, err
	}

	err = io.WriteU64(stream, uint64(userInfo.Stats.RScore))
	if err != nil {
		return nil, err
	}

	err = io.WriteF32(stream, userInfo.Stats.Accuracy)
	if err != nil {
		return nil, err
	}

	err = io.WriteU32(stream, int64(userInfo.Stats.PlayCount))
	if err != nil {
		return nil, err
	}

	err = io.WriteU64(stream, uint64(userInfo.Stats.TScore))
	if err != nil {
		return nil, err
	}

	err = io.WriteU32(stream, int64(userInfo.Stats.Rank))
	if err != nil {
		return nil, err
	}

	return []PacketData{{
		Type: constants.BanchoUserStats,
		Data: stream.Data(),
	}}, nil
}

// writeStatusUpdate writes a status update
func (c *B282Client) writeStatusUpdate(status *types.UserStatus) ([]byte, error) {
	stream := io.NewMemoryStream(nil)

	action := c.convertOutputStatus(*status)
	err := io.WriteU8(stream, int(action))
	if err != nil {
		return nil, err
	}

	if action != constants.StatusUnknown {
		err = io.WriteString(stream, status.Text)
		if err != nil {
			return nil, err
		}

		err = io.WriteString(stream, status.BeatmapChecksum)
		if err != nil {
			return nil, err
		}

		err = io.WriteU16(stream, int(status.Mods))
		if err != nil {
			return nil, err
		}
	}

	return stream.Data(), nil
}

// Utility functions

// convertInputStatus converts input status
func (c *B282Client) convertInputStatus(status constants.Status) constants.Status {
	// For b282, status conversion is straightforward
	return status
}

// convertOutputStatus converts output status
func (c *B282Client) convertOutputStatus(status types.UserStatus) constants.Status {
	// For b282, status conversion is straightforward
	return status.Action
}

// FormatChatLink formats a chat link for this client
func (c *B282Client) FormatChatLink(text, url string) string {
	return fmt.Sprintf("[%s %s]", url, text)
}

// ImplementsPacket returns whether this client implements the given packet
func (c *B282Client) ImplementsPacket(packet constants.PacketType) bool {
	// Check if we have handlers for this packet
	switch packet {
	case constants.OsuUserStatus, constants.OsuMessage, constants.OsuExit, constants.OsuPong:
		return true
	case constants.BanchoLoginReply, constants.BanchoMessage, constants.BanchoPing, constants.BanchoUserStats:
		return true
	default:
		return false
	}
}

// Async implementations (placeholder for now)
func (c *B282Client) ReadPacketAsync(ctx context.Context, stream io.AsyncStream) (constants.PacketType, interface{}, error) {
	return 0, nil, fmt.Errorf("async reading not implemented for B282")
}

func (c *B282Client) WritePacketAsync(ctx context.Context, stream io.AsyncStream, packet constants.PacketType, args ...interface{}) error {
	return fmt.Errorf("async writing not implemented for B282")
}
