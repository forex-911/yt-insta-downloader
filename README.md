# YouTube | Instagram | Spotify Downloader

A unified Python script to download videos, reels, posts, and music from YouTube, Instagram, and Spotify — all in one tool.

It auto-detects the platform and handles quality, format, and folder creation automatically.

---

## Installation

### 1. Clone this repository
```bash
git clone https://github.com/forex-911/yt-insta-downloader.git
cd yt-insta-downloader
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

---

## Features

- Auto-detects platform (YouTube / Instagram / Spotify)
- **YouTube**: Choose format (mp4, mp3, wav) and quality (best, 720p, 1080p)
- **Instagram**:
  - Reel → best-quality MP4
  - Post → best-quality image (JPG/PNG)
- **Spotify**:
  - Single track → MP3 file
  - Playlist → auto-creates subfolder with playlist name
- Smart folder management (no duplicate folder creation)
- Automatic dependency install (spotdl, instaloader if missing)

---

## Usage

### Run the script:
```bash
python at-dl.py
```

### Follow the prompts:
```
Enter URL: https://open.spotify.com/track/1hhLL2eWsnPtYCdDjbiRIU
Detected: Spotify
Enter audio quality (high/low): high
Downloading to: C:\Users\<user>\Downloads\yt-dl-spotify
Spotify download complete!
```

---

## Output Folders

| Platform | Output Folder Path |
|----------|-------------------|
| YouTube Video | `~/Downloads/yt-dl-video/` |
| YouTube Audio | `~/Downloads/yt-dl-audio/` |
| Instagram | `~/Downloads/yt-dl-insta/` |
| Spotify | `~/Downloads/yt-dl-spotify/` (playlist subdir) |

---

## Supported Platforms

- YouTube
- Instagram (Reels + Posts)
- Spotify (Tracks + Playlists)
- 1000+ more platforms supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## Requirements

Add this to your `requirements.txt`:

```
yt-dlp
spotipy
pydub
ffmpeg-python
tqdm
instaloader
```

---

## License

MIT License © 2025 [forex-911](https://github.com/forex-911)

---

## Disclaimer

**This tool is provided for personal use and educational purposes only.**

Always respect copyright laws and the terms of service of each platform. The developers are not responsible for misuse of this tool.

---

## Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/forex-911/yt-insta-downloader/issues).

---

## Contact

For questions or support, please open an issue on GitHub.

---

If you find this tool useful, please star the repository!

