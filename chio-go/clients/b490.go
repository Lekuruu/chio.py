package clients

import (
	"context"
	"fmt"

	"github.com/Lekuruu/chio.py/chio-go/constants"
	"github.com/Lekuruu/chio.py/chio-go/io"
	"github.com/Lekuruu/chio.py/chio-go/types"
)

// B490Client represents the b490 client implementation
// b490 now sends the beatmap ID in user status updates and
// can request a list of set IDs inside the beatmap info request.
type B490Client struct {
	*B282Client // Embed B282 to inherit its functionality
}

// NewB490Client creates a new B490 client
func NewB490Client() *B490Client {
	base := NewB282Client()
	base.version = 490
	return &B490Client{B282Client: base}
}

// writeStatusUpdate writes a status update for b490 (overrides B282)
func (c *B490Client) writeStatusUpdate(status *types.UserStatus) ([]byte, error) {
	stream := io.NewMemoryStream(nil)

	err := io.WriteU8(stream, int(status.Action))
	if err != nil {
		return nil, err
	}

	// b490 always includes beatmap update info
	beatmapUpdate := true
	err = io.WriteBoolean(stream, beatmapUpdate)
	if err != nil {
		return nil, err
	}

	if beatmapUpdate {
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

		err = io.WriteU8(stream, int(status.Mode))
		if err != nil {
			return nil, err
		}

		err = io.WriteS32(stream, int64(status.BeatmapID))
		if err != nil {
			return nil, err
		}
	}

	return stream.Data(), nil
}

// readUserStatus reads user status for b490 (overrides B282)
func (c *B490Client) readUserStatus(stream io.Stream) (*types.UserStatus, error) {
	status := &types.UserStatus{}

	action, err := io.ReadU8(stream)
	if err != nil {
		return nil, err
	}
	status.Action = constants.Status(action)

	beatmapUpdate, err := io.ReadBoolean(stream)
	if err != nil {
		return nil, err
	}

	if beatmapUpdate {
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

		mode, err := io.ReadU8(stream)
		if err != nil {
			return nil, err
		}
		status.Mode = constants.Mode(mode)

		beatmapID, err := io.ReadS32(stream)
		if err != nil {
			return nil, err
		}
		status.BeatmapID = int(beatmapID)
	}

	return status, nil
}

// readBeatmapInfoRequest reads a beatmap info request for b490
func (c *B490Client) readBeatmapInfoRequest(stream io.Stream) (*types.BeatmapInfoRequest, error) {
	request := &types.BeatmapInfoRequest{}

	// Read filenames count
	filenamesCount, err := io.ReadU32(stream)
	if err != nil {
		return nil, err
	}

	// Read filenames
	request.Filenames = make([]string, filenamesCount)
	for i := uint32(0); i < filenamesCount; i++ {
		request.Filenames[i], err = io.ReadString(stream)
		if err != nil {
			return nil, err
		}
	}

	// Read IDs count
	idsCount, err := io.ReadU32(stream)
	if err != nil {
		return nil, err
	}

	// Read IDs
	request.IDs = make([]int, idsCount)
	for i := uint32(0); i < idsCount; i++ {
		id, err := io.ReadS32(stream)
		if err != nil {
			return nil, err
		}
		request.IDs[i] = int(id)
	}

	return request, nil
}

// Override handleReadPacket to add b490-specific packets
func (c *B490Client) handleReadPacket(packet constants.PacketType, stream io.Stream) (interface{}, error) {
	switch packet {
	case constants.OsuUserStatus:
		return c.readUserStatus(stream)
	case constants.OsuBeatmapInfoRequest:
		return c.readBeatmapInfoRequest(stream)
	default:
		// Fall back to B282 implementation
		return c.B282Client.handleReadPacket(packet, stream)
	}
}

// Override writeUserStats to use the new status update format
func (c *B490Client) writeUserStats(args ...interface{}) ([]PacketData, error) {
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

	// Use b490's status update format
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

// ImplementsPacket returns whether this client implements the given packet
func (c *B490Client) ImplementsPacket(packet constants.PacketType) bool {
	// B490 supports additional packets
	switch packet {
	case constants.OsuBeatmapInfoRequest:
		return true
	default:
		// Check base B282 implementation
		return c.B282Client.ImplementsPacket(packet)
	}
}

// Async implementations (placeholder for now)
func (c *B490Client) ReadPacketAsync(ctx context.Context, stream io.AsyncStream) (constants.PacketType, interface{}, error) {
	return 0, nil, fmt.Errorf("async reading not implemented for B490")
}

func (c *B490Client) WritePacketAsync(ctx context.Context, stream io.AsyncStream, packet constants.PacketType, args ...interface{}) error {
	return fmt.Errorf("async writing not implemented for B490")
}
