import os
import yt_dlp
import time
from tqdm import tqdm

# ---------------------------------------
# 🔹 Utility: Generate unique file names
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
# 🔹 Main download logic
# ---------------------------------------
def download_video(url, output_format="mp4", quality="best", retries=3):
    base_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    audio_path = os.path.join(base_download_path, "yt_audio_dw")
    video_path = os.path.join(base_download_path, "yt_video_dw")

    os.makedirs(audio_path, exist_ok=True)
    os.makedirs(video_path, exist_ok=True)

    output_dir = audio_path if output_format in ['mp3', 'wav'] else video_path

    # Auto-handle Instagram links
    if "instagram.com" in url:
        output_format = "mp4"
        quality = "best"
        print("📸 Detected Instagram link — using MP4 best quality.\n")

    # Get metadata (safe title)
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = yt_dlp.utils.sanitize_filename(info.get("title", "video"))
    except Exception:
        title = "video"

    # Fixed output template - use actual format extension
    if output_format in ['mp3', 'wav']:
        output_template = os.path.join(output_dir, f"{title}.%(ext)s")
    else:
        # For video, explicitly set the extension to mp4
        output_template = os.path.join(output_dir, f"{title}.{output_format}")

    # Handle duplicates before downloading
    possible_file = os.path.join(output_dir, f"{title}.{output_format}")
    if os.path.exists(possible_file):
        choice = input("⚠️ File exists! Redownload as new copy? (y/n): ").strip().lower()
        if choice == "y":
            possible_file = safe_filename(possible_file)
            title = os.path.splitext(os.path.basename(possible_file))[0]
            if output_format in ['mp3', 'wav']:
                output_template = os.path.join(output_dir, f"{title}.%(ext)s")
            else:
                output_template = os.path.join(output_dir, f"{title}.{output_format}")
            print(f"📁 New copy will be saved as: {os.path.basename(possible_file)}")
        else:
            print("🚫 Skipped download.")
            return

    print(f"\n📥 Downloading: {title}")
    print(f"💾 Saving to: {output_dir}\n")

    # yt-dlp config with proper format selection and merging
    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [],
    }

    if output_format == 'mp4':
        # Force MP4 container and merge audio+video
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        ydl_opts['postprocessor_args'] = ['-c:v', 'copy', '-c:a', 'aac', '-movflags', 'faststart']
    elif output_format in ['mp3', 'wav']:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }]

    # Retry mechanism
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
# 🔹 Entry point for package
# ---------------------------------------
if __name__ == "__main__":
    url = input("Enter video URL: ").strip()
    format_input = input("Enter format (mp4/mp3/wav): ").strip().lower()
    
    # Map numeric input to formats
    format_map = {'1': 'mp4', '2': 'mp3', '3': 'wav'}
    output_format = format_map.get(format_input, format_input)
    
    # Validate format
    if output_format not in ['mp4', 'mp3', 'wav']:
        print(f"⚠️ Invalid format '{format_input}'. Defaulting to mp4.")
        output_format = 'mp4'
    
    quality = input("Enter quality (best/720p/1080p): ").strip().lower()

    download_video(url, output_format, quality)
