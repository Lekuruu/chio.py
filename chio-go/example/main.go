package main

import (
	"fmt"
	"log"

	"github.com/Lekuruu/chio.py/chio-go"
	"github.com/Lekuruu/chio.py/chio-go/clients"
	"github.com/Lekuruu/chio.py/chio-go/constants"
	"github.com/Lekuruu/chio.py/chio-go/io"
	"github.com/Lekuruu/chio.py/chio-go/types"
)

func main() {
	fmt.Println("Chio.py Go - Bancho Protocol Library")
	fmt.Println("=====================================")

	// Show supported client versions
	fmt.Println("\n--- Supported Client Versions ---")
	for _, info := range chio.GetClientInfo() {
		fmt.Printf("Version %d (%s): %s\n", info.Version, info.Name, info.Description)
	}

	// Test client selection
	fmt.Println("\n--- Testing Client Selection ---")

	// Select by version
	client282, err := chio.SelectClient(282)
	if err != nil {
		log.Printf("Failed to select client: %v", err)
	} else {
		fmt.Printf("Selected client for version 282: version %d\n", client282.Version())
	}

	client490, err := chio.SelectClient(490)
	if err != nil {
		log.Printf("Failed to select client: %v", err)
	} else {
		fmt.Printf("Selected client for version 490: version %d\n", client490.Version())
	}

	// Test latest client
	latest := chio.SelectLatestClient()
	fmt.Printf("Latest client version: %d\n", latest.Version())

	// Create some test data
	userInfo := &types.UserInfo{
		ID:   1,
		Name: "TestUser",
		Status: types.UserStatus{
			Action:          constants.StatusPlaying,
			Text:            "Playing a beatmap",
			Mode:            constants.ModeOsu,
			BeatmapID:       123456,
			BeatmapChecksum: "abcd1234",
		},
		Stats: types.UserStats{
			Rank:      1337,
			RScore:    1000000,
			TScore:    5000000,
			Accuracy:  98.5,
			PlayCount: 1000,
			PP:        4000,
		},
	}

	fmt.Println("\n--- Comparing Client Implementations ---")

	// Test B282 client
	fmt.Println("B282 Client:")
	b282 := clients.NewB282Client()
	testClient(b282, userInfo)

	// Test B490 client
	fmt.Println("\nB490 Client:")
	b490 := clients.NewB490Client()
	testClient(b490, userInfo)

	// Test version differences
	fmt.Println("\n--- Testing Version-Specific Features ---")

	// B490 supports beatmap info requests
	fmt.Printf("B282 supports BeatmapInfoRequest: %t\n", b282.ImplementsPacket(constants.OsuBeatmapInfoRequest))
	fmt.Printf("B490 supports BeatmapInfoRequest: %t\n", b490.ImplementsPacket(constants.OsuBeatmapInfoRequest))

	fmt.Println("\n--- Testing IO Functions ---")

	// Test basic IO functions
	stream := io.NewMemoryStream(nil)

	// Write some test data
	io.WriteString(stream, "Hello, World!")
	io.WriteS32(stream, 12345)
	io.WriteF32(stream, 3.14159)
	io.WriteBoolean(stream, true)

	// Reset stream position for reading
	readStream := io.NewMemoryStream(stream.Data())

	// Read the data back
	str, _ := io.ReadString(readStream)
	num, _ := io.ReadS32(readStream)
	float, _ := io.ReadF32(readStream)
	boolean, _ := io.ReadBoolean(readStream)

	fmt.Printf("String: %s\n", str)
	fmt.Printf("Number: %d\n", num)
	fmt.Printf("Float: %f\n", float)
	fmt.Printf("Boolean: %t\n", boolean)

	fmt.Println("\n--- Testing Packet Features ---")

	// Test packet type functions
	fmt.Printf("BanchoMessage is server packet: %t\n", constants.BanchoMessage.IsServerPacket())
	fmt.Printf("OsuUserStatus is client packet: %t\n", constants.OsuUserStatus.IsClientPacket())
	fmt.Printf("BanchoMessage max size: %d\n", constants.BanchoMessage.MaxSize())
	fmt.Printf("BanchoMessage handler name: %s\n", constants.BanchoMessage.HandlerName())

	// Test types
	fmt.Printf("User avatar filename: %s\n", userInfo.AvatarFilename())

	message := &types.Message{
		Sender:   "BanchoBot",
		Content:  "Welcome to osu!",
		Target:   "#osu",
		SenderID: 1,
	}
	fmt.Printf("Message is DM: %t\n", message.IsDirectMessage())

	// Test presence
	presence := &types.UserPresence{
		CountryIndex: 0,
		City:         "Test City",
		Timezone:     24,
	}
	fmt.Printf("Country string: %s\n", presence.CountryString())

	// Test enum functions
	fmt.Printf("Mode formatted: %s\n", constants.ModeOsu.Formatted())
	fmt.Printf("Mode alias: %s\n", constants.ModeTaiko.Alias())

	fmt.Println("\nExample completed successfully!")
}

func testClient(client chio.BanchoIO, userInfo *types.UserInfo) {
	fmt.Printf("  Version: %d\n", client.Version())

	// Test writing packets
	loginBytes, err := chio.WritePacketToBytes(client, constants.BanchoLoginReply, userInfo.ID)
	if err != nil {
		log.Printf("  Failed to write login reply: %v", err)
	} else {
		fmt.Printf("  Login reply packet size: %d bytes\n", len(loginBytes))
	}

	userStatsBytes, err := chio.WritePacketToBytes(client, constants.BanchoUserStats, userInfo)
	if err != nil {
		log.Printf("  Failed to write user stats: %v", err)
	} else {
		fmt.Printf("  User stats packet size: %d bytes\n", len(userStatsBytes))
	}

	pingBytes, err := chio.WritePacketToBytes(client, constants.BanchoPing)
	if err != nil {
		log.Printf("  Failed to write ping: %v", err)
	} else {
		fmt.Printf("  Ping packet size: %d bytes\n", len(pingBytes))
	}

	fmt.Printf("  Slot size: %d, Header size: %d\n", client.SlotSize(), client.HeaderSize())
}
