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

	// Create a B282 client
	client := clients.NewB282Client()
	fmt.Printf("Client version: %d\n", client.Version())

	// Create some test data
	userInfo := &types.UserInfo{
		ID:   1,
		Name: "TestUser",
		Status: types.UserStatus{
			Action: constants.StatusPlaying,
			Text:   "Playing a beatmap",
			Mode:   constants.ModeOsu,
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

	// Test writing packets
	fmt.Println("\n--- Testing Packet Writing ---")
	
	// Write a login reply packet
	loginBytes, err := chio.WritePacketToBytes(client, constants.BanchoLoginReply, userInfo.ID)
	if err != nil {
		log.Printf("Failed to write login reply: %v", err)
	} else {
		fmt.Printf("Login reply packet size: %d bytes\n", len(loginBytes))
	}

	// Write a message packet
	message := &types.Message{
		Sender:   "BanchoBot",
		Content:  "Welcome to osu!",
		Target:   "#osu",
		SenderID: 1,
	}

	messageBytes, err := chio.WritePacketToBytes(client, constants.BanchoMessage, message)
	if err != nil {
		log.Printf("Failed to write message: %v", err)
	} else {
		fmt.Printf("Message packet size: %d bytes\n", len(messageBytes))
	}

	// Write user stats packet
	statsBytes, err := chio.WritePacketToBytes(client, constants.BanchoUserStats, userInfo)
	if err != nil {
		log.Printf("Failed to write user stats: %v", err)
	} else {
		fmt.Printf("User stats packet size: %d bytes\n", len(statsBytes))
	}

	// Test ping packet
	pingBytes, err := chio.WritePacketToBytes(client, constants.BanchoPing)
	if err != nil {
		log.Printf("Failed to write ping: %v", err)
	} else {
		fmt.Printf("Ping packet size: %d bytes\n", len(pingBytes))
	}

	fmt.Println("\n--- Testing Packet Features ---")

	// Test packet type functions
	fmt.Printf("BanchoMessage is server packet: %t\n", constants.BanchoMessage.IsServerPacket())
	fmt.Printf("OsuUserStatus is client packet: %t\n", constants.OsuUserStatus.IsClientPacket())
	fmt.Printf("BanchoMessage max size: %d\n", constants.BanchoMessage.MaxSize())
	fmt.Printf("BanchoMessage handler name: %s\n", constants.BanchoMessage.HandlerName())

	// Test types
	fmt.Printf("User avatar filename: %s\n", userInfo.AvatarFilename())
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

	fmt.Println("\n--- Client Features ---")
	fmt.Printf("Implements BanchoMessage: %t\n", client.ImplementsPacket(constants.BanchoMessage))
	fmt.Printf("Implements OsuUserStatus: %t\n", client.ImplementsPacket(constants.OsuUserStatus))
	fmt.Printf("Slot size: %d\n", client.SlotSize())
	fmt.Printf("Header size: %d\n", client.HeaderSize())
	fmt.Printf("Auto-join channels: %v\n", client.AutojoinChannels())

	fmt.Println("\nExample completed successfully!")
}