package chio

import (
	"fmt"

	"github.com/Lekuruu/chio.py/chio-go/clients"
)

// SelectClient selects the appropriate client implementation based on version
func SelectClient(version int) (BanchoIO, error) {
	switch {
	case version >= 490:
		return clients.NewB490Client(), nil
	case version >= 282:
		return clients.NewB282Client(), nil
	default:
		return nil, fmt.Errorf("unsupported client version: %d", version)
	}
}

// SelectLatestClient returns the latest supported client implementation
func SelectLatestClient() BanchoIO {
	return clients.NewB490Client()
}

// SelectInitialClient returns the initial client implementation (b282)
func SelectInitialClient() BanchoIO {
	return clients.NewB282Client()
}

// GetSupportedVersions returns a list of all supported client versions
func GetSupportedVersions() []int {
	return []int{282, 490}
}

// IsVersionSupported checks if a client version is supported
func IsVersionSupported(version int) bool {
	supportedVersions := GetSupportedVersions()
	for _, v := range supportedVersions {
		if v == version {
			return true
		}
	}
	return false
}

// ClientInfo represents information about a client version
type ClientInfo struct {
	Version         int
	Name            string
	Description     string
	ProtocolVersion int
}

// GetClientInfo returns information about available client implementations
func GetClientInfo() []ClientInfo {
	return []ClientInfo{
		{
			Version:         282,
			Name:            "b282",
			Description:     "Initial implementation of the bancho protocol",
			ProtocolVersion: 0,
		},
		{
			Version:         490,
			Name:            "b490",
			Description:     "Adds beatmap ID in user status updates and extended beatmap info requests",
			ProtocolVersion: 0,
		},
	}
}
