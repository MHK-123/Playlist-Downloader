import os
import sys
import subprocess
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
    def download(url: str, output_dir: Path) -> bool:

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
    main()
