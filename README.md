# 🎧 Music Playlist Downloader (Spotify & YouTube)

> Clean, minimal, and easy-to-use script for downloading playlists from Spotify and YouTube using `spotdl`.

---

## ✨ Overview

A small, focused CLI tool (Python) that wraps `spotdl` to download entire playlists to a local folder. Designed for reliability and simplicity drop a playlist URL, choose where to save, and let the script do the rest.

Perfect if you want an offline copy of your favourite playlists for personal use.

---

## 🔑 Features

* Detects Spotify and YouTube playlist URLs automatically.
* Uses `spotdl` under the hood for high-quality downloads.
* Creates target directories automatically.
* Streams `spotdl` output to the console so you can watch progress live.
* Cross-platform path-friendly defaults (Windows example provided).

---

## 🧰 Requirements

* Python 3.8+ (recommended)
* `spotdl` installed and available on `PATH` (install with `pip install spotdl`)

Optional but useful:

* `ffmpeg` installed (if you want more control over audio conversion/quality)

---

## 🚀 Quickstart

1. Clone or download this repository.
2. Ensure dependencies are installed:

```bash
pip install spotdl
```

(Install `ffmpeg` if you don't already have it.)

3. Run the script:

```bash
python downloader.py
```

Follow the prompts: paste a playlist URL, then choose an output folder (or press Enter to use the default).

---

## 🔍 Supported URL examples

* Spotify playlist: `https://open.spotify.com/playlist/xxxxxxxxxx`
* Spotify URI: `spotify:playlist:xxxxxxxxxx`
* YouTube playlist: `https://www.youtube.com/playlist?list=PLxxxxx`
* Short YT URL: `https://youtu.be/xxxx?list=PLxxxxx`
* YouTube Music playlist: `https://music.youtube.com/playlist?list=xxxxx`

The script will attempt to detect platform automatically.

---

## ⚙️ Configuration

Modify these top-level constants in the script if you want to change defaults:

```python
DEFAULT_OUTPUT = r"~/Music"
SEPARATOR = "=" * 60
```

You can also pass a different output path interactively when prompted.

---

## 🛠️ How it works (brief)

1. The script validates the provided URL against a few known playlist patterns.
2. If `spotdl` is available, the script runs it as a subprocess inside the chosen output directory.
3. stdout from `spotdl` is printed live, and the script returns a success/failure code.

---

## ✅ Example session

```
Supported platforms:
  • Spotify: https://open.spotify.com/playlist/xxxxx
  • YouTube: https://youtube.com/playlist?list=xxxxx
  • YouTube Music: https://music.youtube.com/playlist?list=xxxxx

Enter playlist URL: https://open.spotify.com/playlist/xxxxxxxx
✓ Detected: Spotify playlist

Output folder (default: ~/Music):
Downloading to: ~/Music
Please wait...
============================================================
...spotdl output...
============================================================
✓ Download complete!
✓ Location: ~/Music
```

---

## 🧯 Troubleshooting

* **`spotdl`**** not found**: run `pip install spotdl` and ensure Python's Scripts folder is in your `PATH`.
* **Permission errors writing to folder**: choose a folder where your user has write permissions or run the script as an elevated user.
* **`ffmpeg`**** errors or poor audio**: install or update `ffmpeg` and make sure it's on `PATH`.
* **Partial or failed downloads**: check the `spotdl` output printed by the script for details.

---

## 🤝 Contributing

Small changes only — this is a light wrapper around `spotdl`.

If you want to improve it:

* Add CLI flags (argparse) instead of interactive prompts.
* Add logging to file (instead of only printing to console).
* Support batch-processing of multiple playlists from a file.

PRs welcome.

---

## 📜 License

MIT — use responsibly and respect content owners' terms of service.

---

## 🙏 Credit

Built around `spotdl` — huge thanks to its maintainers and contributors.

---

### Need it prettier or want a badge-ified version for GitHub? — I can make a README with shields, a table of contents, and example images.
