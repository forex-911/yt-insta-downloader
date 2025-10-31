# YouTube Video Downloader

A simple Python script to download videos and audio from YouTube, Instagram, and other platforms.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/forex-911/yt-insta-downloader.git
cd yt-insta-downloader
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install FFmpeg:

   * **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   * **macOS**: `brew install ffmpeg`
   * **Linux**: `sudo apt install ffmpeg`

## Usage

Run the script:

```bash
python yt-dl.py
```

Follow the prompts:

1. Enter video URL
2. Choose format: `1` (MP4), `2` (MP3), or `3` (WAV)
3. Choose quality: `best`, `720p`, or `1080p`

### Example

```
Enter video URL: https://youtu.be/dQw4w9WgXcQ
Enter format (mp4/mp3/wav): 1
Enter quality (best/720p/1080p): best

✅ Download complete!
```

## Output Folders

* Videos: `~/Downloads/yt_video_dw/`
* Audio: `~/Downloads/yt_audio_dw/`

## Supported Platforms

YouTube, Instagram, Facebook, Twitter, TikTok, Vimeo, and [1000+ more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## License

MIT License

## Disclaimer

For personal use only. Respect copyright laws
