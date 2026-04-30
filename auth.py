from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import os

from db import db
from vars import *

# Command to add a new user
async def add_user_cmd(client: Client, message: Message):
    """Add a new user to the bot"""
    try:
        # Check if sender is admin
        if not db.is_admin(message.from_user.id):
            await message.reply_text(AUTH_MESSAGES["not_admin"])
            return

        # Parse command arguments: /add 123456789 30
        args = message.text.split()[1:]
        if len(args) < 2:
            await message.reply_text(
                AUTH_MESSAGES["invalid_format"].format(
                    format="/add user_id days\nExample: /add 123456789 30"
                )
            )
            return

        user_id = int(args[0])
        days = int(args[1])
        bot_username = client.me.username

        try:
            # Try to get user info from Telegram
            user = await client.get_users(user_id)
            name = user.first_name
            if user.last_name:
                name += f" {user.last_name}"
        except:
            name = f"User {user_id}"

        # Add user to database
        success, expiry_date = db.add_user(user_id, name, days, bot_username)
        
        if success:
            expiry_str = expiry_date.strftime("%d-%m-%Y")
            
            # Notify Admin
            await message.reply_text(
                AUTH_MESSAGES["user_added"].format(
                    name=name,
                    user_id=user_id,
                    expiry_date=expiry_str
                )
            )

            # Notify User
            try:
                await client.send_message(
                    user_id,
                    AUTH_MESSAGES["subscription_active"].format(
                        expiry_date=expiry_str
                    )
                )
            except: pass
        else:
            await message.reply_text("❌ Database update failed.")

    except ValueError:
        await message.reply_text("❌ User ID aur Days sirf numbers mein likhein.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Command to remove a user
async def remove_user_cmd(client: Client, message: Message):
    """Remove a user from the bot"""
    if not db.is_admin(message.from_user.id):
        await message.reply_text("❌ Only Admins can do this.")
        return

    args = message.text.split()[1:]
    if not args:
        await message.reply_text("❌ Format: /remove user_id")
        return

    try:
        user_id = int(args[0])
        if db.remove_user(user_id, client.me.username):
            await message.reply_text(f"✅ User {user_id} removed successfully.")
        else:
            await message.reply_text(f"❌ User not found in database.")
    except:
        await message.reply_text("❌ Invalid User ID.")

# Command to list all users
async def list_users_cmd(client: Client, message: Message):
    """List all authorized users"""
    if not db.is_admin(message.from_user.id):
        await message.reply_text("❌ Admin Access Required.")
        return

    users = db.users.find({"bot_username": client.me.username})
    user_list = await users.to_list(length=100) if hasattr(users, 'to_list') else list(users)
    
    if not user_list:
        await message.reply_text("📝 No authorized users found.")
        return

    msg = "**📝 Authorized Users List**\n\n"
    for user in user_list:
        expiry = user['expiry_date']
        msg += f"👤 **{user.get('name', 'User')}**\nID: `{user['user_id']}`\nExpires: `{expiry.strftime('%d-%m-%Y')}`\n\n"
    
    await message.reply_text(msg)

# Command to check user's plan
async def my_plan_cmd(client: Client, message: Message):
    """Show user's current plan details"""
    user = db.users.find_one({"user_id": message.from_user.id, "bot_username": client.me.username})
    
    if not user:
        # Check if admin/owner
        if message.from_user.id == OWNER_ID or message.from_user.id in ADMINS:
            await message.reply_text("👑 **Admin Status:** Lifetime Unlimited Access.")
            return
        await message.reply_text("❌ You don't have an active subscription.")
        return

    expiry = user['expiry_date']
    days_left = (expiry - datetime.now()).days
    
    await message.reply_text(
        f"**📱 Your Plan Details**\n\n"
        f"👤 **Name:** {user.get('name')}\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"⏳ **Days Left:** {days_left if days_left > 0 else 0}\n"
        f"📅 **Expiry:** {expiry.strftime('%d-%m-%Y')}"
    )
