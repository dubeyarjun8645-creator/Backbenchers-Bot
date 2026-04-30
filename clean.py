import os
import glob
from pathlib import Path
from pyrogram import Client, filters
from vars import ADMINS, OWNER_ID
from db import db
from datetime import datetime
from pyrogram.handlers import MessageHandler

def clean_downloads():
    """Clean everything in downloads directory"""
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        
        for file in glob.glob("downloads/*"):
            try:
                if os.path.isfile(file):
                    os.remove(file)
            except Exception: pass
    except Exception as e:
        print(f"Error cleaning downloads: {e}")

def clean_media_files():
    """Clean images and videos except wm.png"""
    try:
        # Media and temp formats
        formats = ["*.jpg", "*.jpeg", "*.png", "*.mp4", "*.mkv", "*.webm", "*.part", "*.ytdl"]
        
        for pattern in formats:
            for file in glob.glob(pattern):
                try:
                    # Protect watermark and important files
                    if file in ["wm.png", "font.otf", "youtube_cookies.txt"]:
                        continue
                    if os.path.isfile(file):
                        os.remove(file)
                except Exception: pass
    except Exception as e:
        print(f"Error cleaning media files: {e}")

def clean_all():
    """Clean all temporary files"""
    clean_downloads()
    clean_media_files()

async def clean_expired_users(client: Client):
    """Clean expired users and notify them"""
    try:
        # Get all users (Using the db instance logic from db.py)
        removed_count = 0
        now = datetime.now()
        
        # Simplified logic matching your Database class
        expired_users = db.users.find({
            "expiry_date": {"$lt": now},
            "user_id": {"$nin": [OWNER_ID] + ADMINS}
        })
        
        for user in expired_users:
            try:
                # Notify user before removal
                await client.send_message(
                    user['user_id'],
                    "**⚠️ Your subscription has expired**\n\nYour access has been revoked. Contact admin to renew."
                )
                db.users.delete_one({"_id": user["_id"]})
                removed_count += 1
            except Exception:
                db.users.delete_one({"_id": user["_id"]})
                removed_count += 1
                
        return removed_count
    except Exception as e:
        print(f"Error cleaning users: {e}")
        return 0

async def handle_clean_command(client: Client, message):
    """Handle /clean command for admins"""
    if not db.is_admin(message.from_user.id):
        await message.reply_text("⚠️ Access Denied.")
        return
        
    status_msg = await message.reply_text("🧹 Cleaning system...")
    clean_all()
    removed = await clean_expired_users(client)
    
    await status_msg.edit_text(
        f"✅ **Cleanup Successful**\n\n"
        f"• Temp files removed\n"
        f"• {removed} expired users cleared"
    )

def register_clean_handler(bot: Client):
    """Register the handler in main.py"""
    bot.add_handler(MessageHandler(handle_clean_command, filters.command("clean") & filters.private))

# Run initial clean on startup
clean_all()
