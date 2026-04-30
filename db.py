import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union
from pymongo import MongoClient, errors
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection
from vars import *
import colorama
from colorama import Fore, Style
import time
import certifi

# Init colors
colorama.init()

class Database:
    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0):
        self.client: Optional[MongoClient] = None
        self.db: Optional[MongoDatabase] = None
        self.users: Optional[Collection] = None
        self.settings: Optional[Collection] = None
        self.bot_settings: Optional[Collection] = None
        
        self._connect_with_retry(max_retries, retry_delay)
        
    def _connect_with_retry(self, max_retries: int, retry_delay: float):
        for attempt in range(1, max_retries + 1):
            try:
                print(f"{Fore.YELLOW}⌛ Attempt {attempt}: Connecting to MongoDB...{Style.RESET_ALL}")
                self.client = MongoClient(
                    MONGO_URL,
                    serverSelectionTimeoutMS=20000,
                    tlsCAFile=certifi.where()
                )
                self.client.server_info() # Test connection
                
                # Standard database name from vars or default
                db_name = os.environ.get("DATABASE_NAME", "UGxPRO")
                self.db = self.client.get_database(db_name)
                self.users = self.db['users']
                self.settings = self.db['user_settings']
                self.bot_settings = self.db['bot_settings']
                
                print(f"{Fore.GREEN}✓ MongoDB Connected Successfully!{Style.RESET_ALL}")
                self._create_indexes()
                return
            except Exception as e:
                print(f"{Fore.RED}✕ Connection attempt {attempt} failed: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries: time.sleep(retry_delay)
                else: raise

    def _create_indexes(self):
        try:
            self.users.create_index([("bot_username", 1), ("user_id", 1)], unique=True)
            self.users.create_index("expiry_date", expireAfterSeconds=0)
        except: pass

    def is_user_authorized(self, user_id: int, bot_username: str = "ugdevbot") -> bool:
        if user_id == OWNER_ID or user_id in ADMINS: return True
        user = self.users.find_one({"user_id": user_id, "bot_username": bot_username})
        if not user or 'expiry_date' not in user: return False
        return user['expiry_date'] > datetime.now()

    def is_admin(self, user_id: int) -> bool:
        return user_id == OWNER_ID or user_id in ADMINS

    def add_user(self, user_id: int, name: str, days: int, bot_username: str = "ugdevbot"):
        expiry_date = datetime.now() + timedelta(days=days)
        self.users.update_one(
            {"user_id": user_id, "bot_username": bot_username},
            {"$set": {"name": name, "expiry_date": expiry_date, "last_updated": datetime.now()}},
            upsert=True
        )
        return True, expiry_date

    def remove_user(self, user_id: int, bot_username: str = "ugdevbot"):
        result = self.users.delete_one({"user_id": user_id, "bot_username": bot_username})
        return result.deleted_count > 0

    def get_log_channel(self, bot_username: str):
        settings = self.bot_settings.find_one({"bot_username": bot_username})
        return settings.get('log_channel') if settings else None

    def set_log_channel(self, bot_username: str, channel_id: int):
        self.bot_settings.update_one(
            {"bot_username": bot_username},
            {"$set": {"log_channel": channel_id}},
            upsert=True
        )
        return True

# Initialize the db object for other files to import
db = Database()
