import os
import sys
import shlex
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

os.environ["PATH"] += os.pathsep + r"C:\\ffmpeg\\bin"

APP_TITLE = "YouTube Downloader — mp3 / mp4"


class YTDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        pad = 8
        frm = ttk.Frame(self, padding=pad)
        frm.grid(row=0, column=0, sticky="nsew")

        # URL
        ttk.Label(frm, text="YouTube URL:").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(frm, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, pad))

        # Format
        ttk.Label(frm, text="Format:").grid(row=2, column=0, sticky="w")
        self.format_var = tk.StringVar(value="mp4")
        r1 = ttk.Radiobutton(frm, text="MP4 (video)", variable=self.format_var, value="mp4")
        r2 = ttk.Radiobutton(frm, text="MP3 (audio)", variable=self.format_var, value="mp3")
        r1.grid(row=3, column=0, sticky="w")
        r2.grid(row=3, column=1, sticky="w")

        # Output folder
        ttk.Label(frm, text="Output folder:").grid(row=4, column=0, sticky="w")
        self.output_var = tk.StringVar(value=os.path.expanduser("~"))
        self.output_entry = ttk.Entry(frm, textvariable=self.output_var, width=45)
        self.output_entry.grid(row=5, column=0, sticky="w")
        ttk.Button(frm, text="Browse", command=self.browse_output).grid(row=5, column=1, sticky="w")

        # Options
        self.keep_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="Keep video file when extracting audio", variable=self.keep_var).grid(row=6, column=0, columnspan=2, sticky="w")

        # Download button
        self.download_btn = ttk.Button(frm, text="Download", command=self.on_download)
        self.download_btn.grid(row=7, column=0, pady=(pad, 0))

        # Progress / log
        ttk.Label(frm, text="Log / progress:").grid(row=8, column=0, sticky="w", pady=(pad//2, 0))
        self.log = tk.Text(frm, width=70, height=12, state="disabled")
        self.log.grid(row=9, column=0, columnspan=3, pady=(0, pad))

    def browse_output(self):
        d = filedialog.askdirectory(initialdir=self.output_var.get())
        if d:
            self.output_var.set(d)

    def append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def on_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please paste a YouTube URL.")
            return
        outdir = self.output_var.get().strip()
        if not outdir or not os.path.isdir(outdir):
            messagebox.showwarning("Bad output folder", "Please choose a valid output folder.")
            return

        fmt = self.format_var.get()
        keep_video = self.keep_var.get()

        # Disable button while downloading
        self.download_btn.configure(state="disabled")
        t = threading.Thread(target=self.download_thread, args=(url, outdir, fmt, keep_video), daemon=True)
        t.start()

    def download_thread(self, url, outdir, fmt, keep_video):
        try:
            self.append_log(f"Starting download: {url}")

            # Build yt-dlp command
            # output template: title.ext in chosen folder
            outtmpl = os.path.join(outdir, "%(title)s.%(ext)s")

            if fmt == "mp4": #mp4
                cmd = [sys.executable, "-m", "yt_dlp", "-f", "bestvideo+bestaudio/best", "-o", outtmpl, url]
            else:  # mp3
                cmd = [sys.executable, "-m", "yt_dlp", "--extract-audio", "--audio-format", "mp3", "--audio-quality", "0", "-o", outtmpl, url]

            # Run process and capture output line by line
            self.append_log("Running: " + " ".join(shlex.quote(x) for x in cmd))

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

            # Read output
            for line in proc.stdout:
                line = line.rstrip("\n")
                self.append_log(line)

            proc.wait()
            if proc.returncode == 0:
                self.append_log("Download finished successfully.")
                messagebox.showinfo("Done", "Download finished successfully.")
            else:
                self.append_log(f"yt-dlp exited with code {proc.returncode}")
                messagebox.showerror("Error", f"yt-dlp exited with code {proc.returncode}. Check log for details.")

        except FileNotFoundError as e:
            self.append_log("ERROR: yt-dlp or python -m yt_dlp not found.")
            self.append_log(str(e))
            messagebox.showerror("Missing dependency", "yt-dlp (or python -m yt_dlp) not found. Install via: pip install yt-dlp\nAlso make sure ffmpeg is installed and on PATH.")
        except Exception as e:
            self.append_log("ERROR: " + str(e))
            messagebox.showerror("Error", str(e))
        finally:
            # re-enable button
            self.download_btn.configure(state="normal")


if __name__ == "__main__":
    app = YTDownloader()
    app.mainloop()
