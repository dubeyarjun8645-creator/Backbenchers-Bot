import os
from os import environ

# API Configuration
API_ID = int(os.environ.get("API_ID", "34338736"))
API_HASH = os.environ.get("API_HASH", "cb0624172e5db326489e1855a83d0c26")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8735659924:AAGAYER6YNgxAgzd3Wr4suxwgIQbgFzcch8")

CREDIT = os.environ.get("CREDIT", "𓍯Arjun⚝")

# MongoDB Configuration
# UPDATE: Removed the syntax error here (DATABASE_NAME = DATABASE_NAME = ...)
DATABASE_NAME = os.environ.get("DATABASE_NAME", "UGxPRO")
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://DemoArjun:Arjun496333@cluster0.mrmyunr.mongodb.net/?appName=Cluster0")
MONGO_URL = DATABASE_URL  # For auth system

# Owner and Admin Configuration
OWNER_ID = int(os.environ.get("OWNER_ID", "8606649929"))
ADMINS = [7973698690, 8269675690]  # List of admin IDs

# Channel Configuration
PREMIUM_CHANNEL = "https://t.me/+IB4WJmz0n4QxMjFl"

# Thumbnail Configuration
THUMBNAILS = os.environ.get("THUMBNAILS", "https://i.fbcd.co/products/original/ug-logo-designs-2-acbfbf7b80e16df4c902a34d1caf148e7e1feca736e21075114990e62294f3ac.jpg").split()

# Web Server Configuration
WEB_SERVER = os.environ.get("WEB_SERVER", "False").lower() == "true"
WEBHOOK = True  
PORT = int(os.environ.get("PORT", 8000))

# Message Formats
AUTH_MESSAGES = {
    "subscription_active": """<b>🎉 Subscription Activated!</b>
<blockquote>Your subscription has been activated and will expire on {expiry_date}.
You can now use the bot!</blockquote>\n\n Type /start to start uploading """,

    "subscription_expired": """<b>⚠️ Your Subscription Has Ended</b>
<blockquote>Your access to the bot has been revoked as your subscription period has expired.
Please contact the admin to renew your subscription.</blockquote>""",

    "user_added": """<b>✅ User Added Successfully!</b>
<blockquote>👤 Name: {name}
🆔 User ID: {user_id}
📅 Expiry: {expiry_date}</blockquote>""",

    "user_removed": """<b>✅ User Removed Successfully!</b>
<blockquote>User ID {user_id} has been removed from authorized users.</blockquote>""",

    "access_denied": """<b>⚠️ Access Denied!</b>
<blockquote>You are not authorized to use this bot.
Please contact the admin @ItsUGBot to get access.</blockquote>""",

    "not_admin": "⚠️ You are not authorized to use this command!",
    
    "invalid_format": """❌ <b>Invalid Format!</b>
<blockquote>Use format: {format}</blockquote>"""
}





