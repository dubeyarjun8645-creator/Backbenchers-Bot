import os
import time
import math
import subprocess
import asyncio
import aiohttp
import aiofiles
import requests
import m3u8
from pathlib import Path
from urllib.parse import urljoin
from vars import CREDIT, db # Importing db instance from vars or db
from utils import progress_bar

# Render path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# build.sh installs tools in the 'bin' folder
MP4DECRYPT = os.path.join(BASE_DIR, "bin", "mp4decrypt")

# Ensure downloads directory exists for thumbnails/temp files
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def duration(filename):
    """Get video duration using ffprobe"""
    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return float(result.stdout)
    except:
        return 0

async def download(url, name):
    """Download PDF or small files"""
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka

async def split_file(file_path, chunk_size_mb=1900):
    """Split files larger than 2GB for Telegram"""
    file_size = os.path.getsize(file_path)
    chunk_size = chunk_size_mb * 1024 * 1024
    if file_size <= chunk_size:
        return [file_path]
    
    num_chunks = math.ceil(file_size / chunk_size)
    base_name = os.path.splitext(file_path)[0]
    ext = os.path.splitext(file_path)[1]
    split_files = []
    
    dur = duration(file_path)
    segment_duration = dur / num_chunks
    
    for i in range(num_chunks):
        output_file = f"{base_name}_part{i+1}{ext}"
        start_time = i * segment_duration
        # Fast seeking with -ss before -i
        cmd = f'ffmpeg -ss {start_time} -t {segment_duration} -i "{file_path}" -c copy "{output_file}" -y'
        os.system(cmd)
        if os.path.exists(output_file):
            split_files.append(output_file)
    
    return split_files if split_files else [file_path]

async def decrypt_and_merge_video(mpd_url, keys_string, output_path, output_name, quality="480"):
    """DRM Decryption logic using mp4decrypt"""
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Check if mp4decrypt exists
    tool = MP4DECRYPT if os.path.exists(MP4DECRYPT) else "mp4decrypt"

    # 1. Download encrypted streams
    cmd1 = f'yt-dlp -f "bv[height<={quality}]+ba/b" --allow-unplayable-format -o "{output_path}/encrypted.%(ext)s" "{mpd_url}"'
    os.system(cmd1)

    # 2. Decrypt
    for file in output_path.glob("encrypted.*"):
        if file.suffix == ".mp4":
            os.system(f'{tool} {keys_string} "{file}" "{output_path}/video.mp4"')
        elif file.suffix in [".m4a", ".webm"]:
            os.system(f'{tool} {keys_string} "{file}" "{output_path}/audio.m4a"')
        file.unlink()

    # 3. Merge
    final_file = output_path / f"{output_name}.mp4"
    os.system(f'ffmpeg -i "{output_path}/video.mp4" -i "{output_path}/audio.m4a" -c copy "{final_file}" -y')
    
    # Cleanup temp parts
    for temp in ["video.mp4", "audio.m4a"]:
        temp_path = output_path / temp
        if temp_path.exists(): temp_path.unlink()
        
    return str(final_file)

async def download_video(url, cmd, name):
    """Standard downloader using yt-dlp + aria2c"""
    # Adding aria2c for faster speed on Render
    download_cmd = f'{cmd} --external-downloader aria2c --downloader-args "aria2c:-x 16 -s 16 -j 16"'
    os.system(download_cmd)
    
    # Find the downloaded file
    for ext in ['mp4', 'mkv', 'webm']:
        file_path = f"{name}.{ext}"
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 2000 * 1024 * 1024:
                return await split_file(file_path)
            return [file_path]
    return [f"{name}.mp4"]

async def send_vid(bot, m, cc, filename, thumb, name, prog, channel_id, watermark=""):
    """Final uploader to Telegram"""
    files = filename if isinstance(filename, list) else [filename]
    await prog.delete()

    for i, file in enumerate(files):
        status = await m.reply_text(f"📤 **Uploading Part {i+1}...**")
        start_time = time.time()
        
        # Thumbnail Logic
        current_thumb = thumb
        if thumb == "/d" or not os.path.exists(str(thumb)):
            current_thumb = f"downloads/thumb_{i}.jpg"
            os.system(f'ffmpeg -i "{file}" -ss 00:00:05 -vframes 1 "{current_thumb}" -y')

        try:
            dur = int(duration(file))
            await bot.send_video(
                chat_id=channel_id,
                video=file,
                caption=f"{cc}\n\n**Part {i+1}**" if len(files) > 1 else cc,
                duration=dur,
                thumb=current_thumb if os.path.exists(str(current_thumb)) else None,
                supports_streaming=True,
                progress=progress_bar,
                progress_args=(status, start_time)
            )
        except Exception as e:
            await m.reply_text(f"❌ **Upload Error:** {str(e)}")
        
        # Cleanup
        if os.path.exists(file): os.remove(file)
        if current_thumb and "downloads/thumb_" in current_thumb and os.path.exists(current_thumb):
            os.remove(current_thumb)
        await status.delete()
