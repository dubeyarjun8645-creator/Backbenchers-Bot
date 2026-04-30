# 🚀 UGx Uploader Bot v2.0

Advanced DRM Video Uploader Bot for Telegram with MongoDB Authorization and High-Speed Downloading.

## 🛠 Features
- **DRM Decryption:** Support for decrypted video streams (mp4decrypt).
- **Auto Splitting:** Automatically splits videos larger than 2GB for Telegram.
- **Fast Downloading:** Integrated with `aria2c` for maximum speed.
- **Auth System:** MongoDB-based user subscription management.
- **Web Interface:** Flask-powered keep-alive page for 24/7 uptime.
- **Cleanup System:** Auto-deletes junk files to save disk space.

---

## 📂 Repository Structure
```text
├── main.py           # Core bot logic
├── vars.py           # Configuration & Credentials
├── ug.py             # Download & DRM Engine
├── db.py             # MongoDB Database Handler
├── auth.py           # User Authorization Commands
├── utils.py          # Progress Bar & Helpers
├── logs.py           # Error Logging System
├── clean.py          # File Cleanup System
├── app.py            # Flask Web Server
├── apixug.py         # Secure API Client
├── build.sh          # Tool Installer (ffmpeg, yt-dlp)
└── requirements.txt  # Python Dependencies
