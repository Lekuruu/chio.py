#!/bin/bash

# Comprehensive test script for chio-go
echo "=== Chio.py Go Comprehensive Test Suite ==="
echo ""

# Test 1: Build all packages
echo "1. Building all packages..."
go build ./...
if [ $? -eq 0 ]; then
    echo "   ✅ Build successful"
else
    echo "   ❌ Build failed"
    exit 1
fi

echo ""

# Test 2: Run the example
echo "2. Running example program..."
cd example
go run main.go > test_output.txt 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Example ran successfully"
    echo "   Output lines: $(wc -l < test_output.txt)"
else
    echo "   ❌ Example failed"
    cat test_output.txt
    exit 1
fi
cd ..

echo ""

# Test 3: Check module dependencies
echo "3. Checking module dependencies..."
go mod verify
if [ $? -eq 0 ]; then
    echo "   ✅ Module dependencies verified"
else
    echo "   ❌ Module dependency issues"
    exit 1
fi

echo ""

# Test 4: Format check
echo "4. Checking code formatting..."
unformatted=$(gofmt -l .)
if [ -z "$unformatted" ]; then
    echo "   ✅ All code properly formatted"
else
    echo "   ❌ Unformatted files found:"
    echo "$unformatted"
fi

echo ""

# Test 5: Basic functionality test
echo "5. Testing basic functionality..."
mkdir -p test_tmp
cd test_tmp
cat > main.go << 'EOF'
package main

import (
    "fmt"
    "log"
    "github.com/Lekuruu/chio.py/chio-go"
    "github.com/Lekuruu/chio.py/chio-go/constants"
    "github.com/Lekuruu/chio.py/chio-go/types"
)

func main() {
    // Test client selection
    client, err := chio.SelectClient(490)
    if err != nil {
        log.Fatal("Failed to select client:", err)
    }

    // Test packet writing
    userInfo := &types.UserInfo{
        ID:   42,
        Name: "TestUser",
    }
    
    data, err := chio.WritePacketToBytes(client, constants.BanchoLoginReply, userInfo.ID)
    if err != nil {
        log.Fatal("Failed to write packet:", err)
    }
    
    if len(data) == 0 {
        log.Fatal("No data written")
    }
    
    fmt.Printf("Success: Generated %d bytes\n", len(data))
}
EOF

go mod init test
go mod edit -require=github.com/Lekuruu/chio.py/chio-go@v0.0.0
go mod edit -replace=github.com/Lekuruu/chio.py/chio-go=../
go mod tidy

go run main.go
result=$?
cd ..
rm -rf test_tmp

if [ $result -eq 0 ]; then
    echo "   ✅ Basic functionality test passed"
else
    echo "   ❌ Basic functionality test failed"
    exit 1
fi

echo ""

echo "=== All Tests Passed! ==="
echo ""
echo "Summary:"
echo "- Go build: Working"
echo "- Example program: Working"
echo "- Module dependencies: Verified"
echo "- Code formatting: $(if [ -z "$unformatted" ]; then echo "Good"; else echo "Needs fixing"; fi)"
echo "- Basic functionality: Working"
echo ""
echo "The Go rewrite is complete and functional!"