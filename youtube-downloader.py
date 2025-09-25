import customtkinter as ctk
import threading
import yt_dlp
import os
from tkinter import filedialog, messagebox

# ======= MANUAL FFMPEG PATH =======
# Enter the path to ffmpeg/bin on your system
FFMPEG_PATH = r"C:\\ffmpeg\\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# ======= APPEARANCE SETTINGS =======
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# ======= FUNCTIONS =======
def choose_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_path_var.set(folder)

def download_video():
    url = url_entry.get()
    folder = output_path_var.get()
    file_format = format_var.get()

    if not url.strip():
        messagebox.showwarning("Error", "Please enter a YouTube URL!")
        return

    if not folder.strip():
        messagebox.showwarning("Error", "Please choose an output folder!")
        return

    threading.Thread(target=run_download, args=(url, folder, file_format), daemon=True).start()

def run_download(url, folder, file_format):
    progress_bar.set(0)
    status_label.configure(text="⏳ Downloading...")

    ydl_opts = {
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True  # Download only a single video
    }

    if file_format == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.configure(text="✅ Download completed successfully!")
    except Exception as e:
        status_label.configure(text="❌ Error")
        messagebox.showerror("Error", str(e))

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 1)
            percent = downloaded / total
            progress_bar.set(percent)
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.set(1)

# ======= MAIN WINDOW =======
app = ctk.CTk()
app.geometry("600x550")
app.title("🎶 YouTube Downloader by RXSOON")

# ======= UI ELEMENTS =======
title_label = ctk.CTkLabel(
    app, text="🎧 YouTube Downloader 🎧",
    font=("Century Gothic", 28, "bold"),
    text_color="#4B4453"
)
title_label.pack(pady=20)

# URL entry
url_entry = ctk.CTkEntry(
    app, placeholder_text="Paste YouTube URL",
    width=450, height=40, corner_radius=15
)
url_entry.pack(pady=10)

# Format selection
format_var = ctk.StringVar(value="mp3")
format_frame = ctk.CTkFrame(app, corner_radius=15)
format_frame.pack(pady=10)
ctk.CTkRadioButton(format_frame, text="🎵 MP3", variable=format_var, value="mp3").pack(side="left", padx=20, pady=10)
ctk.CTkRadioButton(format_frame, text="🎬 MP4", variable=format_var, value="mp4").pack(side="left", padx=20, pady=10)

# Output folder selection
output_path_var = ctk.StringVar(value=os.getcwd())
folder_btn = ctk.CTkButton(
    app, text="📂 Choose Folder",
    command=choose_output_folder,
    corner_radius=20, fg_color="#B5FFFC", text_color="black"
)
folder_btn.pack(pady=10)

# Download button
download_btn = ctk.CTkButton(
    app, text="⬇️ Download",
    command=download_video,
    width=200, height=50,
    corner_radius=25, fg_color="#FFDEE9", text_color="black"
)
download_btn.pack(pady=20)

# Progress bar
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# Status label
status_label = ctk.CTkLabel(app, text="", font=("Century Gothic", 14))
status_label.pack(pady=5)

# Start the app
app.mainloop()
