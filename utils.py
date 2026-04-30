import time
import math
import os
from vars import CREDIT  
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta

class Timer:  
    def __init__(self, time_between=5):  
        self.start_time = time.time()  
        self.time_between = time_between  

    def can_send(self):  
        if time.time() > (self.start_time + self.time_between):  
            self.start_time = time.time()  
            return True  
        return False  

def hrb(value, digits=2, delim="", postfix=""):  
    """Return a human-readable file size."""  
    if value is None:  
        return None  
    chosen_unit = "B"  
    for unit in ("KB", "MB", "GB", "TB"):  
        if value > 1000:  
            value /= 1024  
            chosen_unit = unit  
        else:  
            break  
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix  

def hrt(seconds, precision=0):  
    """Return a human-readable time delta as a string."""  
    pieces = []  
    value = timedelta(seconds=seconds)  

    if value.days:  
        pieces.append(f"{value.days}d")  

    seconds = value.seconds  

    if seconds >= 3600:  
        hours = int(seconds / 3600)  
        pieces.append(f"{hours}h")  
        seconds -= hours * 3600  

    if seconds >= 60:  
        minutes = int(seconds / 60)  
        pieces.append(f"{minutes}m")  
        seconds -= minutes * 60  

    if seconds > 0 or not pieces:  
        pieces.append(f"{seconds}s")  

    if not precision:  
        return "".join(pieces)  

    return "".join(pieces[:precision])  

timer = Timer()  

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return

        # Calculations
        perc = f"{current * 100 / total:.1f}%"
        speed = hrb(current / diff, postfix="/s")
        eta = hrt(int((total - current) / (current / diff))) if current > 0 else "0s"
        
        # Modern progress bar design
        bar_length = 11
        filled_length = int(current * bar_length / total)
        remaining_length = bar_length - filled_length
        
        filled = "█" * filled_length
        remaining = "░" * remaining_length
        p_bar = f"{filled}{remaining}"

        # Final UI Layout
        msg = (
            f"**🚀 Uploading Progress**\n\n"
            f"<blockquote>"
            f"<b>📊 Percentage :</b> {perc}\n"
            f"<b>📈 Speed :</b> {speed}\n"
            f"<b>⏳ ETA :</b> {eta}\n"
            f"</blockquote>\n"
            f"`{p_bar}`\n\n"
            f"✨ **Powered by :** {CREDIT}"
        )

        try:
            await reply.edit(msg)
        except FloodWait as e:
            time.sleep(e.x)
        except Exception:
            pass
