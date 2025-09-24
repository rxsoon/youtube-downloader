# YouTube Downloader — MP3 / MP4

A simple Python GUI tool for downloading YouTube videos as **MP4 (video)** or **MP3 (audio)** using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

![screenshot](screenshot.png)

---

## ✨ Features

* Download YouTube videos in **MP4 (video)** format
* Extract **MP3 (audio)** with high quality (requires ffmpeg)
* Simple and clean Tkinter-based GUI
* Choose output folder
* Shows live log of the yt-dlp process

---

## 🚀 Installation

### Requirements

* Python 3.8+
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [ffmpeg](https://ffmpeg.org/) (must be installed and added to PATH)

### Setup

```bash
# clone the repo
git clone https://github.com/rxsoon/youtube-downloader.git
cd youtube-downloader

# install dependencies
pip install yt-dlp
```

---

## ▶️ Usage

Run the app:

```bash
python youtube_downloader.py
```

1. Paste the YouTube URL
2. Select output format (**MP4** or **MP3**)
3. Choose output folder
4. Click **Download**

---

## 📦 Build Executable (optional)

If you want a standalone app (no need to install Python), you can use [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile youtube_downloader.py
```

The executable will be in the `dist/` folder.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Download videos **only if you have the rights** to do so. The author is not responsible for misuse.


