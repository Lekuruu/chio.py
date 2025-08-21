package io

import (
	"bytes"
	"compress/gzip"
	"context"
	"encoding/binary"
	"fmt"
	"io"
	"log"
	"math"
)

// Logger for IO operations
var Logger = log.Default()

// Stream represents an abstract stream for I/O operations
type Stream interface {
	Read(size int) ([]byte, error)
	Write(data []byte) error
}

// AsyncStream represents an abstract stream for asynchronous I/O operations
type AsyncStream interface {
	ReadAsync(ctx context.Context, size int) ([]byte, error)
	WriteAsync(ctx context.Context, data []byte) error
}

// MemoryStream implements Stream using an in-memory buffer
type MemoryStream struct {
	data     []byte
	position int
}

// NewMemoryStream creates a new memory stream
func NewMemoryStream(data []byte) *MemoryStream {
	return &MemoryStream{
		data:     data,
		position: 0,
	}
}

// Read reads data from the stream
func (ms *MemoryStream) Read(size int) ([]byte, error) {
	if size == -1 {
		size = len(ms.data) - ms.position
	}

	if ms.position+size > len(ms.data) {
		return nil, fmt.Errorf("attempt to read beyond stream bounds")
	}

	result := make([]byte, size)
	copy(result, ms.data[ms.position:ms.position+size])
	ms.position += size
	return result, nil
}

// Write writes data to the stream
func (ms *MemoryStream) Write(data []byte) error {
	ms.data = append(ms.data, data...)
	return nil
}

// Data returns the stream data
func (ms *MemoryStream) Data() []byte {
	return ms.data
}

// Clear clears the stream
func (ms *MemoryStream) Clear() {
	ms.data = nil
	ms.position = 0
}

// Available returns the number of available bytes
func (ms *MemoryStream) Available() int {
	return len(ms.data) - ms.position
}

// Utility functions for clamping values
func clampInt8(value int) int8 {
	if value < -0x80 {
		return -0x80
	}
	if value > 0x7F {
		return 0x7F
	}
	return int8(value)
}

func clampUint8(value int) uint8 {
	if value < 0 {
		return 0
	}
	if value > 0xFF {
		return 0xFF
	}
	return uint8(value)
}

func clampInt16(value int) int16 {
	if value < -0x8000 {
		return -0x8000
	}
	if value > 0x7FFF {
		return 0x7FFF
	}
	return int16(value)
}

func clampUint16(value int) uint16 {
	if value < 0 {
		return 0
	}
	if value > 0xFFFF {
		return 0xFFFF
	}
	return uint16(value)
}

func clampInt32(value int64) int32 {
	if value < -0x80000000 {
		return -0x80000000
	}
	if value > 0x7FFFFFFF {
		return 0x7FFFFFFF
	}
	return int32(value)
}

func clampUint32(value int64) uint32 {
	if value < 0 {
		return 0
	}
	if value > 0xFFFFFFFF {
		return 0xFFFFFFFF
	}
	return uint32(value)
}

// Read functions

// ReadS8 reads a signed 8-bit integer
func ReadS8(stream Stream) (int8, error) {
	data, err := stream.Read(1)
	if err != nil {
		return 0, err
	}
	return int8(data[0]), nil
}

// ReadU8 reads an unsigned 8-bit integer
func ReadU8(stream Stream) (uint8, error) {
	data, err := stream.Read(1)
	if err != nil {
		return 0, err
	}
	return data[0], nil
}

// ReadS16 reads a signed 16-bit integer (little endian)
func ReadS16(stream Stream) (int16, error) {
	data, err := stream.Read(2)
	if err != nil {
		return 0, err
	}
	return int16(binary.LittleEndian.Uint16(data)), nil
}

// ReadU16 reads an unsigned 16-bit integer (little endian)
func ReadU16(stream Stream) (uint16, error) {
	data, err := stream.Read(2)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint16(data), nil
}

// ReadS32 reads a signed 32-bit integer (little endian)
func ReadS32(stream Stream) (int32, error) {
	data, err := stream.Read(4)
	if err != nil {
		return 0, err
	}
	return int32(binary.LittleEndian.Uint32(data)), nil
}

// ReadU32 reads an unsigned 32-bit integer (little endian)
func ReadU32(stream Stream) (uint32, error) {
	data, err := stream.Read(4)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint32(data), nil
}

// ReadS64 reads a signed 64-bit integer (little endian)
func ReadS64(stream Stream) (int64, error) {
	data, err := stream.Read(8)
	if err != nil {
		return 0, err
	}
	return int64(binary.LittleEndian.Uint64(data)), nil
}

// ReadU64 reads an unsigned 64-bit integer (little endian)
func ReadU64(stream Stream) (uint64, error) {
	data, err := stream.Read(8)
	if err != nil {
		return 0, err
	}
	return binary.LittleEndian.Uint64(data), nil
}

// ReadBoolean reads a boolean value
func ReadBoolean(stream Stream) (bool, error) {
	value, err := ReadU8(stream)
	if err != nil {
		return false, err
	}
	return value != 0, nil
}

// ReadF32 reads a 32-bit float (little endian)
func ReadF32(stream Stream) (float32, error) {
	data, err := stream.Read(4)
	if err != nil {
		return 0, err
	}
	bits := binary.LittleEndian.Uint32(data)
	return math.Float32frombits(bits), nil
}

// ReadF64 reads a 64-bit float (little endian)
func ReadF64(stream Stream) (float64, error) {
	data, err := stream.Read(8)
	if err != nil {
		return 0, err
	}
	bits := binary.LittleEndian.Uint64(data)
	return math.Float64frombits(bits), nil
}

// ReadGzip reads and decompresses gzip data
func ReadGzip(stream Stream, size int) ([]byte, error) {
	var data []byte
	var err error
	
	if size == -1 {
		// Read all available data
		if ms, ok := stream.(*MemoryStream); ok {
			data, err = stream.Read(ms.Available())
		} else {
			return nil, fmt.Errorf("cannot read all data from non-memory stream")
		}
	} else {
		data, err = stream.Read(size)
	}
	
	if err != nil {
		return nil, err
	}

	reader, err := gzip.NewReader(bytes.NewReader(data))
	if err != nil {
		return nil, err
	}
	defer reader.Close()

	return io.ReadAll(reader)
}

// ReadULEB128 reads an unsigned LEB128 encoded integer
func ReadULEB128(stream Stream) (int, error) {
	num := 0
	shift := 0

	for {
		b, err := ReadU8(stream)
		if err != nil {
			return 0, err
		}

		num |= (int(b) & 0x7F) << shift
		if (b & 0x80) == 0 {
			break
		}
		shift += 7
	}

	return num, nil
}

// ReadString reads a string
func ReadString(stream Stream) (string, error) {
	empty, err := ReadU8(stream)
	if err != nil {
		return "", err
	}

	if empty == 0x00 {
		return "", nil
	}

	size, err := ReadULEB128(stream)
	if err != nil {
		return "", err
	}

	data, err := stream.Read(size)
	if err != nil {
		return "", err
	}

	return string(data), nil
}

// ReadBoolList reads a list of booleans from a byte
func ReadBoolList(stream Stream, size int) ([]bool, error) {
	if size == 0 {
		size = 8
	}

	b, err := ReadU8(stream)
	if err != nil {
		return nil, err
	}

	result := make([]bool, size)
	for i := 0; i < size; i++ {
		result[i] = ((b >> i) & 1) > 0
	}

	return result, nil
}

// ReadListS32 reads a list of 32-bit signed integers
func ReadListS32(stream Stream) ([]int32, error) {
	count, err := ReadS32(stream)
	if err != nil {
		return nil, err
	}

	result := make([]int32, count)
	for i := int32(0); i < count; i++ {
		result[i], err = ReadS32(stream)
		if err != nil {
			return nil, err
		}
	}

	return result, nil
}

// ReadListS16 reads a list of 32-bit signed integers with 16-bit count
func ReadListS16(stream Stream) ([]int32, error) {
	count, err := ReadU16(stream)
	if err != nil {
		return nil, err
	}

	result := make([]int32, count)
	for i := uint16(0); i < count; i++ {
		result[i], err = ReadS32(stream)
		if err != nil {
			return nil, err
		}
	}

	return result, nil
}

// Write functions

// WriteS8 writes a signed 8-bit integer
func WriteS8(stream Stream, value int) error {
	data := []byte{byte(clampInt8(value))}
	return stream.Write(data)
}

// WriteU8 writes an unsigned 8-bit integer
func WriteU8(stream Stream, value int) error {
	data := []byte{clampUint8(value)}
	return stream.Write(data)
}

// WriteS16 writes a signed 16-bit integer (little endian)
func WriteS16(stream Stream, value int) error {
	data := make([]byte, 2)
	binary.LittleEndian.PutUint16(data, uint16(clampInt16(value)))
	return stream.Write(data)
}

// WriteU16 writes an unsigned 16-bit integer (little endian)
func WriteU16(stream Stream, value int) error {
	data := make([]byte, 2)
	binary.LittleEndian.PutUint16(data, clampUint16(value))
	return stream.Write(data)
}

// WriteS32 writes a signed 32-bit integer (little endian)
func WriteS32(stream Stream, value int64) error {
	data := make([]byte, 4)
	binary.LittleEndian.PutUint32(data, uint32(clampInt32(value)))
	return stream.Write(data)
}

// WriteU32 writes an unsigned 32-bit integer (little endian)
func WriteU32(stream Stream, value int64) error {
	data := make([]byte, 4)
	binary.LittleEndian.PutUint32(data, clampUint32(value))
	return stream.Write(data)
}

// WriteS64 writes a signed 64-bit integer (little endian)
func WriteS64(stream Stream, value int64) error {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, uint64(value))
	return stream.Write(data)
}

// WriteU64 writes an unsigned 64-bit integer (little endian)
func WriteU64(stream Stream, value uint64) error {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, value)
	return stream.Write(data)
}

// WriteBoolean writes a boolean value
func WriteBoolean(stream Stream, value bool) error {
	if value {
		return WriteU8(stream, 1)
	}
	return WriteU8(stream, 0)
}

// WriteF32 writes a 32-bit float (little endian)
func WriteF32(stream Stream, value float32) error {
	data := make([]byte, 4)
	binary.LittleEndian.PutUint32(data, math.Float32bits(value))
	return stream.Write(data)
}

// WriteF64 writes a 64-bit float (little endian)
func WriteF64(stream Stream, value float64) error {
	data := make([]byte, 8)
	binary.LittleEndian.PutUint64(data, math.Float64bits(value))
	return stream.Write(data)
}

// WriteGzip compresses and writes gzip data
func WriteGzip(stream Stream, data []byte) error {
	var buf bytes.Buffer
	writer := gzip.NewWriter(&buf)
	
	_, err := writer.Write(data)
	if err != nil {
		return err
	}
	
	err = writer.Close()
	if err != nil {
		return err
	}
	
	return stream.Write(buf.Bytes())
}

// WriteULEB128 writes an unsigned LEB128 encoded integer
func WriteULEB128(stream Stream, value int) error {
	if value == 0 {
		return stream.Write([]byte{0x00})
	}

	var result []byte
	for value != 0 {
		b := byte(value & 0x7F)
		value >>= 7
		if value != 0 {
			b |= 0x80
		}
		result = append(result, b)
	}

	return stream.Write(result)
}

// WriteString writes a string
func WriteString(stream Stream, value string) error {
	if value == "" {
		return WriteU8(stream, 0x00)
	}

	err := WriteU8(stream, 0x0B)
	if err != nil {
		return err
	}

	data := []byte(value)
	err = WriteULEB128(stream, len(data))
	if err != nil {
		return err
	}

	return stream.Write(data)
}

// WriteBoolList writes a list of booleans as a byte
func WriteBoolList(stream Stream, values []bool) error {
	if len(values) > 8 {
		return fmt.Errorf("bool list too long: %d (max 8)", len(values))
	}

	var b byte
	for i, value := range values {
		if value {
			b |= 1 << i
		}
	}

	return WriteU8(stream, int(b))
}

// WriteListS32 writes a list of 32-bit signed integers
func WriteListS32(stream Stream, values []int32) error {
	err := WriteS32(stream, int64(len(values)))
	if err != nil {
		return err
	}

	for _, value := range values {
		err = WriteS32(stream, int64(value))
		if err != nil {
			return err
		}
	}

	return nil
}

// WriteListS16 writes a list of 32-bit signed integers with 16-bit count
func WriteListS16(stream Stream, values []int32) error {
	err := WriteU16(stream, len(values))
	if err != nil {
		return err
	}

	for _, value := range values {
		err = WriteS32(stream, int64(value))
		if err != nil {
			return err
		}
	}

	return nil
}