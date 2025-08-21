package chio

import (
	"context"
	"fmt"

	"github.com/Lekuruu/chio.py/chio-go/constants"
	"github.com/Lekuruu/chio.py/chio-go/io"
)

// BanchoIO is the main interface that wraps the basic methods for
// reading and writing packets to a Bancho client.
type BanchoIO interface {
	// Version information
	Version() int
	SlotSize() int
	HeaderSize() int
	ProtocolVersion() int
	DisableCompression() bool
	RequiresStatusUpdates() bool
	AutojoinChannels() []string

	// Packet operations
	ReadPacket(stream io.Stream) (constants.PacketType, interface{}, error)
	WritePacket(stream io.Stream, packet constants.PacketType, args ...interface{}) error
	ReadPacketAsync(ctx context.Context, stream io.AsyncStream) (constants.PacketType, interface{}, error)
	WritePacketAsync(ctx context.Context, stream io.AsyncStream, packet constants.PacketType, args ...interface{}) error

	// Chat formatting
	FormatChatLink(text, url string) string

	// Utility methods
	ImplementsPacket(packet constants.PacketType) bool
}

// PacketResult represents the result of reading a packet
type PacketResult struct {
	Type constants.PacketType
	Data interface{}
}

// BaseBanchoIO provides a base implementation of BanchoIO
type BaseBanchoIO struct {
	version               int
	slotSize              int
	headerSize            int
	protocolVersion       int
	disableCompression    bool
	requiresStatusUpdates bool
	autojoinChannels      []string
}

// NewBaseBanchoIO creates a new base BanchoIO implementation
func NewBaseBanchoIO() *BaseBanchoIO {
	return &BaseBanchoIO{
		version:               0,
		slotSize:              8,
		headerSize:            6,
		protocolVersion:       0,
		disableCompression:    false,
		requiresStatusUpdates: true,
		autojoinChannels:      []string{"#osu", "#announce"},
	}
}

// Version returns the client version
func (b *BaseBanchoIO) Version() int {
	return b.version
}

// SlotSize returns the slot size
func (b *BaseBanchoIO) SlotSize() int {
	return b.slotSize
}

// HeaderSize returns the header size
func (b *BaseBanchoIO) HeaderSize() int {
	return b.headerSize
}

// ProtocolVersion returns the protocol version
func (b *BaseBanchoIO) ProtocolVersion() int {
	return b.protocolVersion
}

// DisableCompression returns whether compression is disabled
func (b *BaseBanchoIO) DisableCompression() bool {
	return b.disableCompression
}

// RequiresStatusUpdates returns whether status updates are required
func (b *BaseBanchoIO) RequiresStatusUpdates() bool {
	return b.requiresStatusUpdates
}

// AutojoinChannels returns the channels to auto-join
func (b *BaseBanchoIO) AutojoinChannels() []string {
	return b.autojoinChannels
}

// ReadPacket reads a packet from the stream (to be implemented by clients)
func (b *BaseBanchoIO) ReadPacket(stream io.Stream) (constants.PacketType, interface{}, error) {
	return constants.PacketType(0), nil, fmt.Errorf("ReadPacket not implemented")
}

// WritePacket writes a packet to the stream (to be implemented by clients)
func (b *BaseBanchoIO) WritePacket(stream io.Stream, packet constants.PacketType, args ...interface{}) error {
	return fmt.Errorf("WritePacket not implemented")
}

// ReadPacketAsync reads a packet from the stream asynchronously
func (b *BaseBanchoIO) ReadPacketAsync(ctx context.Context, stream io.AsyncStream) (constants.PacketType, interface{}, error) {
	// Default implementation - to be overridden by specific clients if needed
	return constants.PacketType(0), nil, fmt.Errorf("ReadPacketAsync not implemented")
}

// WritePacketAsync writes a packet to the stream asynchronously
func (b *BaseBanchoIO) WritePacketAsync(ctx context.Context, stream io.AsyncStream, packet constants.PacketType, args ...interface{}) error {
	// Default implementation - to be overridden by specific clients if needed
	return fmt.Errorf("WritePacketAsync not implemented")
}

// FormatChatLink formats a chat link for this client
func (b *BaseBanchoIO) FormatChatLink(text, url string) string {
	// Default implementation - to be overridden by specific clients
	return fmt.Sprintf("[%s %s]", url, text)
}

// ImplementsPacket returns whether the current client version implements the given packet
func (b *BaseBanchoIO) ImplementsPacket(packet constants.PacketType) bool {
	// This would need to be implemented by checking if the handler exists
	// For now, return false as default
	return false
}

// ReadPacketFromBytes reads a packet from the given bytes
func ReadPacketFromBytes(client BanchoIO, data []byte) (constants.PacketType, interface{}, error) {
	stream := io.NewMemoryStream(data)
	return client.ReadPacket(stream)
}

// ReadManyPacketsFromBytes reads multiple packets from the given bytes
func ReadManyPacketsFromBytes(client BanchoIO, data []byte) ([]PacketResult, error) {
	stream := io.NewMemoryStream(data)
	var results []PacketResult

	for stream.Available() >= client.HeaderSize() {
		packetType, data, err := client.ReadPacket(stream)
		if err != nil {
			return results, err
		}

		results = append(results, PacketResult{
			Type: packetType,
			Data: data,
		})
	}

	return results, nil
}

// WritePacketToBytes encodes a packet and returns it as bytes
func WritePacketToBytes(client BanchoIO, packet constants.PacketType, args ...interface{}) ([]byte, error) {
	stream := io.NewMemoryStream(nil)
	err := client.WritePacket(stream, packet, args...)
	if err != nil {
		return nil, err
	}
	return stream.Data(), nil
}

// WriteManyPacketsToBytes encodes multiple packets and returns them as bytes
func WriteManyPacketsToBytes(client BanchoIO, packets []PacketResult) ([]byte, error) {
	stream := io.NewMemoryStream(nil)

	for _, packet := range packets {
		err := client.WritePacket(stream, packet.Type, packet.Data)
		if err != nil {
			return nil, err
		}
	}

	return stream.Data(), nil
}
