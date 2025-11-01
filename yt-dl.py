import os
import yt_dlp
import time
import subprocess
import json
from tqdm import tqdm

# ---------------------------------------
# 🔹 Utility: Safe filename
# ---------------------------------------
def safe_filename(path):
    base, ext = os.path.splitext(path)
    count = 2
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base} ({count}){ext}"
        count += 1
    return new_path


# ---------------------------------------
# 🔹 tqdm-compatible progress bar
# ---------------------------------------
def progress_hook(tq):
    def hook(d):
        if d['status'] == 'downloading':
            if d.get('total_bytes'):
                tq.total = d['total_bytes']
            elif d.get('total_bytes_estimate'):
                tq.total = d['total_bytes_estimate']
            tq.n = d.get('downloaded_bytes', 0)
            tq.set_postfix(speed=d.get('_speed_str', ''), eta=d.get('_eta_str', ''))
            tq.refresh()
        elif d['status'] == 'finished':
            tq.n = tq.total
            tq.close()
    return hook


# ---------------------------------------
# 🔹 YouTube / Instagram Downloader
# ---------------------------------------
def download_ytdlp(url, output_format="mp4", quality="best", retries=3):
    user_home = os.path.expanduser("~")
    base_download_path = os.path.join(user_home, "Downloads")

    # Select folder dynamically
    if "instagram.com" in url:
        output_dir = os.path.join(base_download_path, "al-dl-insta")
    elif output_format in ['mp3', 'wav']:
        output_dir = os.path.join(base_download_path, "al-dl-audio")
    else:
        output_dir = os.path.join(base_download_path, "al-dl-video")

    os.makedirs(output_dir, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = yt_dlp.utils.sanitize_filename(info.get("title", "video"))
    except Exception:
        title = "video"

    output_template = os.path.join(output_dir, f"{title}.%(ext)s")
    possible_file = os.path.join(output_dir, f"{title}.{output_format}")

    if os.path.exists(possible_file):
        choice = input("⚠️ File exists! Redownload as new copy? (y/n): ").strip().lower()
        if choice == "y":
            possible_file = safe_filename(possible_file)
            title = os.path.splitext(os.path.basename(possible_file))[0]
            output_template = os.path.join(output_dir, f"{title}.%(ext)s")
            print(f"📁 New copy will be saved as: {os.path.basename(possible_file)}")
        else:
            print("🚫 Skipped download.")
            return

    print(f"\n📥 Downloading: {title}")
    print(f"💾 Saving to: {output_dir}\n")

    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [],
    }

    if output_format == 'mp4':
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
        ydl_opts['merge_output_format'] = 'mp4'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
        ydl_opts['postprocessor_args'] = ['-c:v', 'copy', '-c:a', 'aac', '-movflags', 'faststart']

    elif output_format in ['mp3', 'wav']:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }]

    for attempt in range(1, retries + 1):
        try:
            with tqdm(total=0, unit='B', unit_scale=True, desc=f'Attempt {attempt}/{retries}', dynamic_ncols=True) as tq:
                ydl_opts['progress_hooks'] = [progress_hook(tq)]
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            print(f"\n✅ Download complete! Saved in: {output_dir}\n")
            return
        except Exception as e:
            print(f"\n⚠️ Error during download: {e}")
            if attempt < retries:
                print(f"🔁 Retrying in 5 seconds... ({attempt}/{retries})")
                time.sleep(5)
            else:
                print("❌ Download failed after multiple attempts.\n")


# ---------------------------------------
# 🔹 Spotify Downloader (via spotdl)
# ---------------------------------------
def download_spotify(url, quality="high"):
    user_home = os.path.expanduser("~")
    base_dir = os.path.join(user_home, "Downloads", "al-dl-spotify")
    os.makedirs(base_dir, exist_ok=True)

    print("\n🎵 Fetching Spotify data...")

    # Check spotdl presence
    try:
        subprocess.run(["spotdl", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("⚠️ spotdl not found. Installing automatically...")
        subprocess.run(["pip", "install", "spotdl"], check=True)

    # Detect playlist
    playlist_name = None
    if "playlist" in url:
        try:
            meta = subprocess.run(["spotdl", "list", "--url", url, "--json"], capture_output=True, text=True)
            data = json.loads(meta.stdout)
            if isinstance(data, list) and len(data) > 0 and 'name' in data[0]:
                playlist_name = data[0]['name']
        except Exception:
            playlist_name = "playlist"

    # Output directory
    output_dir = os.path.join(base_dir, playlist_name) if playlist_name else base_dir
    os.makedirs(output_dir, exist_ok=True)

    print(f"💾 Downloading to: {output_dir}\n")
    bitrate = "320k" if quality == "high" else "128k"

    cmd = ["spotdl", url, "--output", output_dir, "--bitrate", bitrate]
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Spotify download complete! Files saved in: {output_dir}\n")
    except Exception as e:
        print(f"❌ Spotify download failed: {e}\n")


# ---------------------------------------
# 🔹 Entry Point
# ---------------------------------------
if __name__ == "__main__":
    url = input("Enter URL: ").strip()

    if "youtube.com" in url or "youtu.be" in url:
        print("\n▶️ Detected: YouTube")
        fmt = input("Enter format (mp4/mp3/wav): ").strip().lower()
        if fmt not in ['mp4', 'mp3', 'wav']:
            print("⚠️ Invalid format. Defaulting to mp4.")
            fmt = 'mp4'
        quality = input("Enter quality (best/720p/1080p): ").strip().lower()
        download_ytdlp(url, output_format=fmt, quality=quality)

    elif "instagram.com" in url:
        print("\n📸 Detected: Instagram — using best quality MP4.")
        download_ytdlp(url, output_format="mp4", quality="best")

    elif "spotify.com" in url:
        print("\n🎧 Detected: Spotify")
        quality = input("Enter audio quality (high/low): ").strip().lower()
        if quality not in ['high', 'low']:
            print("⚠️ Invalid quality. Defaulting to high.")
            quality = 'high'
        download_spotify(url, quality)

    else:
        print("❌ Unsupported URL. Only YouTube, Instagram, and Spotify are supported.")
