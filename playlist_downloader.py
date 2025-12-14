import os
import sys
import subprocess
import argparse
import urllib.parse
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
from typing import Tuple, Optional

# Constants
DEFAULT_OUTPUT = Path.home() / "Music"
SEPARATOR = "=" * 60

# URL patterns for validation
URL_PATTERNS = {
    'spotify': ['spotify.com/playlist/', 'spotify:playlist:'],
    'youtube': ['youtube.com/playlist', 'youtu.be/', 'music.youtube.com/playlist']
}

class MusicDownloader:
    """Handles music downloads from Spotify and YouTube."""
    
    @staticmethod
    def check_spotdl() -> bool:
        try:
            result = subprocess.run(
                ['spotdl', '--version'],
                capture_output=True,
                text=True,
                check=False
            )
            print(f"✓ spotdl installed: {result.stdout.strip()}\n")
            return True
        except FileNotFoundError:
            print("✗ spotdl not installed!\n")
            print("Install with: pip install spotdl")
            return False
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        url = url.lower()
        
        for platform, patterns in URL_PATTERNS.items():
            if any(pattern in url for pattern in patterns):
                return True, platform
        
        return False, None

    @staticmethod
    def normalize_url(url: str) -> str:
        try:
            parsed = urllib.parse.urlparse(url)
            qs = urllib.parse.parse_qs(parsed.query)

            # If there's a 'list' query param, build a clean playlist URL with only the id
            if 'list' in qs and qs['list']:
                list_id = qs['list'][0]
                if 'music.youtube.com' in parsed.netloc:
                    return f"https://music.youtube.com/playlist?list={list_id}"
                return f"https://www.youtube.com/playlist?list={list_id}"

            return url
        except Exception:
            return url
    
    @staticmethod
    def download(url: str, output_dir: Path) -> bool:

        # sanitize url (strip extra query params like &si=...)
        url = MusicDownloader.normalize_url(url)

        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Downloading to: {output_dir.absolute()}")
        print("Please wait...\n")
        print(SEPARATOR)
        
        original_dir = os.getcwd()
        
        try:
            os.chdir(output_dir)

            process = subprocess.Popen(
                ['spotdl', url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                print(line, end='')
            
            process.wait()
            
            success = process.returncode == 0
            
            if success:
                print(f"\n{SEPARATOR}")
                print("✓ Download complete!")
                print(f"✓ Location: {output_dir.absolute()}")
                print(SEPARATOR)
            else:
                print("\n✗ Download failed. Check output above.")
            
            return success
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return False
        finally:
            os.chdir(original_dir)

    @staticmethod
    def download_stream(url: str, output_dir: Path, line_callback) -> bool:

        # sanitize url (strip extra query params like &si=...)
        url = MusicDownloader.normalize_url(url)

        output_dir.mkdir(parents=True, exist_ok=True)

        line_callback(f"Downloading to: {output_dir.absolute()}\n")
        line_callback("Please wait...\n\n")
        line_callback(SEPARATOR + "\n")

        original_dir = os.getcwd()

        try:
            os.chdir(output_dir)

            process = subprocess.Popen(
                ['spotdl', url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                line_callback(line)

            process.wait()

            success = process.returncode == 0

            if success:
                line_callback(f"\n{SEPARATOR}\n")
                line_callback("✓ Download complete!\n")
                line_callback(f"✓ Location: {output_dir.absolute()}\n")
                line_callback(SEPARATOR + "\n")
            else:
                line_callback("\n✗ Download failed. Check output above.\n")

            return success

        except Exception as e:
            line_callback(f"\n✗ Error: {e}\n")
            return False
        finally:
            os.chdir(original_dir)

def get_user_input() -> Tuple[str, Path]:

    print("Supported platforms:")
    print("  • Spotify: https://open.spotify.com/playlist/xxxxx")
    print("  • YouTube: https://youtube.com/playlist?list=xxxxx")
    print("  • YouTube Music: https://music.youtube.com/playlist?list=xxxxx\n")

    url = input("Enter playlist URL: ").strip()
    
    if not url:
        print("✗ URL required!")
        sys.exit(1)
    
    # Validate URL
    is_valid, platform = MusicDownloader.validate_url(url)
    
    if not is_valid:
        print("\n✗ Invalid URL!")
        print("Please provide a Spotify or YouTube playlist URL.")
        sys.exit(1)
    
    print(f"✓ Detected: {platform.title()} playlist\n")
    
    # Get output directory
    output_input = input(f"Output folder (default: {DEFAULT_OUTPUT}): ").strip()
    output_dir = Path(output_input) if output_input else Path(DEFAULT_OUTPUT)
    
    print()
    return url, output_dir

def main():
    """Main execution flow."""
    print(SEPARATOR)
    print("  Music Playlist Downloader (Spotify & YouTube)")
    print(SEPARATOR)
    print()
    
    # Check dependencies
    if not MusicDownloader.check_spotdl():
        sys.exit(1)
    
    try:
        # Get inputs
        url, output_dir = get_user_input()
        
        # Download
        downloader = MusicDownloader()
        success = downloader.download(url, output_dir)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music Playlist Downloader (Spotify & YouTube)")
    parser.add_argument('--gui', '-g', action='store_true', help='Launch Tkinter GUI')
    args, unknown = parser.parse_known_args()

    def launch_gui():
        root = tk.Tk()
        root.title("Playlist Downloader ")
        root.geometry("760x520")
        root.configure(bg="#FFFAF0")

        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('TLabel', background='#FFFAF0')
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))

        header = tk.Label(root, text="🎵 Playlist Downloader", font=("Segoe UI", 20, 'bold'), bg='#FFFAF0', fg='#3B3B98')
        header.pack(pady=(12, 6))

        sub = tk.Label(root, text="paste your playlist URL below.", font=("Segoe UI", 10), bg='#FFFAF0', fg='#6B6B6B')
        sub.pack(pady=(0, 12))

        frame = ttk.Frame(root)
        frame.pack(fill='x', padx=16)

        ttk.Label(frame, text="Playlist URL:").grid(row=0, column=0, sticky='w')
        url_var = tk.StringVar()
        url_entry = ttk.Entry(frame, textvariable=url_var, width=72)
        url_entry.grid(row=0, column=1, columnspan=2, padx=8, pady=4, sticky='w')

        ttk.Label(frame, text="Output folder:").grid(row=1, column=0, sticky='w')
        out_var = tk.StringVar(value=str(DEFAULT_OUTPUT))
        out_entry = ttk.Entry(frame, textvariable=out_var, width=56)
        out_entry.grid(row=1, column=1, padx=8, pady=4, sticky='w')

        def browse():
            d = filedialog.askdirectory(initialdir=str(DEFAULT_OUTPUT))
            if d:
                out_var.set(d)

        browse_btn = ttk.Button(frame, text="Browse…", command=browse)
        browse_btn.grid(row=1, column=2, sticky='w')

        status = scrolledtext.ScrolledText(root, height=18, wrap='word', font=("Consolas", 10))
        status.pack(fill='both', expand=True, padx=12, pady=12)

        def append_line(line: str):
            def insert():
                status.insert('end', line)
                status.see('end')
            status.after(0, insert)

        def run_download():
            url = url_var.get().strip()
            if not url:
                messagebox.showerror("Error", "Please provide a playlist URL.")
                download_btn.config(state='normal')
                return

            output_dir = Path(out_var.get())

            if not MusicDownloader.check_spotdl():
                messagebox.showerror("Missing dependency", "spotdl not installed. Install with: pip install spotdl")
                download_btn.config(state='normal')
                return

            append_line(f"Starting download for: {url}\n")

            success = MusicDownloader.download_stream(url, output_dir, append_line)

            if success:
                messagebox.showinfo("Done", f"Download finished. Files in:\n{output_dir}")
            else:
                messagebox.showwarning("Failed", "Download finished with errors. See log.")

            download_btn.config(state='normal')

        def on_download():
            download_btn.config(state='disabled')
            status.delete('1.0', 'end')
            t = threading.Thread(target=run_download, daemon=True)
            t.start()

        download_btn = ttk.Button(root, text="Download playlist", command=on_download)
        download_btn.pack(pady=(0, 12))

        root.mainloop()

    if args.gui:
        launch_gui()
    else:
        main()
