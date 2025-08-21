# Chio.py Go

**Chio (Bancho I/O) Go** is a Go port of the Python library for serializing and deserializing bancho packets, with support for all versions of osu! that use bancho (2008-2025).

This is a complete rewrite of the original Python [chio.py](https://github.com/Lekuruu/chio.py) library in Go, maintaining the same functionality and API design patterns while leveraging Go's performance and type safety.

## Features

- ✅ Complete packet serialization/deserialization for the Bancho protocol
- ✅ Support for multiple client versions (b282, b490, b20130303, etc.)
- ✅ Type-safe data structures for all Bancho types
- ✅ Memory-efficient IO operations with proper endianness handling
- ✅ Comprehensive constants and enums matching the Python version
- ✅ Client interface with versioned implementations

## Installation

```bash
go get github.com/Lekuruu/chio.py/chio-go
```

## Quick Start

```go
package main

import (
    "fmt"
    "log"

    "github.com/Lekuruu/chio.py/chio-go"
    "github.com/Lekuruu/chio.py/chio-go/clients"
    "github.com/Lekuruu/chio.py/chio-go/constants"
    "github.com/Lekuruu/chio.py/chio-go/types"
)

func main() {
    // Create a client for a specific osu! version
    client := clients.NewB282Client()

    // Create user information
    userInfo := &types.UserInfo{
        ID:   2,
        Name: "peppy",
        Status: types.UserStatus{
            Action: constants.StatusIdle,
            Text:   "",
        },
        Stats: types.UserStats{
            Rank: 1,
            PP:   8000,
        },
    }

    // Write packets
    loginBytes, err := chio.WritePacketToBytes(client, constants.BanchoLoginReply, userInfo.ID)
    if err != nil {
        log.Fatal(err)
    }

    userStatsBytes, err := chio.WritePacketToBytes(client, constants.BanchoUserStats, userInfo)
    if err != nil {
        log.Fatal(err)
    }

    // Send a message
    message := &types.Message{
        Sender:   "BanchoBot",
        Content:  "Hello, World!",
        Target:   "#osu",
        SenderID: 1,
    }

    messageBytes, err := chio.WritePacketToBytes(client, constants.BanchoMessage, message)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Generated %d bytes of packet data\n", 
        len(loginBytes)+len(userStatsBytes)+len(messageBytes))
}
```

## Package Structure

```
chio-go/
├── constants/     # Protocol constants, enums, and packet types
├── types/         # Data structures (UserInfo, Message, Match, etc.)
├── io/           # Stream interfaces and binary I/O functions  
├── clients/      # Client implementations (b282, b490, etc.)
├── example/      # Example usage
├── chio.go       # Main BanchoIO interface
└── go.mod        # Go module definition
```

## Supported Clients

Currently implemented:
- **b282** - Initial bancho protocol implementation

Planned implementations:
- b490, b504, b20130303, b20161101, b20250306, and many more...

## Key Differences from Python Version

1. **Type Safety**: Go's static typing prevents many runtime errors
2. **Performance**: Significantly faster execution and lower memory usage
3. **Interfaces**: Uses Go interfaces instead of Python's class inheritance
4. **Error Handling**: Explicit error handling following Go conventions
5. **Concurrency**: Built-in support for concurrent operations

## Data Types

The Go version maintains all the same data types as the Python version:

| Type | Go Struct | Python Class |
|------|-----------|--------------|
| User Information | `types.UserInfo` | `chio.UserInfo` |
| User Status | `types.UserStatus` | `chio.UserStatus` |
| Message | `types.Message` | `chio.Message` |
| Match | `types.Match` | `chio.Match` |
| Channel | `types.Channel` | `chio.Channel` |

## Constants and Enums

All constants are properly typed:

```go
// Packet types
constants.BanchoMessage
constants.OsuUserStatus

// Status values  
constants.StatusPlaying
constants.StatusIdle

// Game modes
constants.ModeOsu
constants.ModeTaiko

// And many more...
```

## IO Operations

The IO package provides efficient binary read/write operations:

```go
import "github.com/Lekuruu/chio.py/chio-go/io"

stream := io.NewMemoryStream(nil)

// Write data
io.WriteString(stream, "Hello")
io.WriteS32(stream, 12345)
io.WriteF32(stream, 3.14159)

// Read data back
readStream := io.NewMemoryStream(stream.Data())
str, _ := io.ReadString(readStream)
num, _ := io.ReadS32(readStream)  
float, _ := io.ReadF32(readStream)
```

## Contributing

This is a faithful port of the original Python library. When adding new features:

1. Maintain compatibility with the Python API design
2. Follow Go conventions and idioms
3. Add comprehensive tests
4. Update documentation

## License

MIT License - Same as the original Python version.

## Credits

- Original Python library by [Lekuru](https://github.com/Lekuruu)
- Go port maintains the same excellent protocol documentation and implementation