#!/bin/bash
set -e

echo "Building all croc versions..."
mkdir -p dist

# Linux
echo "Building Linux versions..."
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-linux-amd64
echo "✓ Linux amd64"

GOOS=linux GOARCH=386 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-linux-386
echo "✓ Linux 386"

GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-linux-arm64
echo "✓ Linux arm64"

GOOS=linux GOARCH=arm GOARM=7 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-linux-arm7
echo "✓ Linux arm7"

# Windows
echo "Building Windows versions..."
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-windows-amd64.exe
echo "✓ Windows amd64"

GOOS=windows GOARCH=386 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-windows-386.exe
echo "✓ Windows 386"

GOOS=windows GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-windows-arm64.exe
echo "✓ Windows arm64"

# macOS
echo "Building macOS versions..."
GOOS=darwin GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-darwin-amd64
echo "✓ macOS amd64"

GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-darwin-arm64
echo "✓ macOS arm64 (Apple Silicon)"

# FreeBSD
echo "Building FreeBSD versions..."
GOOS=freebsd GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-freebsd-amd64
echo "✓ FreeBSD amd64"

GOOS=freebsd GOARCH=386 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-freebsd-386
echo "✓ FreeBSD 386"

# OpenBSD
echo "Building OpenBSD versions..."
GOOS=openbsd GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-openbsd-amd64
echo "✓ OpenBSD amd64"

# NetBSD
echo "Building NetBSD versions..."
GOOS=netbsd GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/croc-netbsd-amd64
echo "✓ NetBSD amd64"

echo ""
echo "Build complete! Built binaries:"
ls -lh dist/
