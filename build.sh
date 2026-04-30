#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create a bin directory for tools
mkdir -p bin

# 1. Download FFmpeg static build
echo "Installing FFmpeg..."
curl -L https://github.com/Bhyve/ffmpeg-static/releases/download/v4.4.1/ffmpeg -o bin/ffmpeg
chmod +x bin/ffmpeg

# 2. Download yt-dlp
echo "Installing yt-dlp..."
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o bin/yt-dlp
chmod +x bin/yt-dlp

# 3. Download mp4decrypt (shaka-packager)
echo "Installing mp4decrypt..."
curl -L https://github.com/shaka-project/shaka-packager/releases/download/v2.6.1/packager-linux-x64 -o bin/mp4decrypt
chmod +x bin/mp4decrypt

# Export the bin folder to PATH so the bot can find the tools
export PATH=$PATH:$(pwd)/bin

echo "✅ All tools installed successfully!"
