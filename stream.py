import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# We get the stream key from environment variables (loaded from .env or Railway)
stream_key = os.environ.get("STREAM_KEY")
if not stream_key:
    print("Error: STREAM_KEY not found in environment variables.")
    sys.exit(1)

# RTMP URL (YouTube default)
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

video_path = "video.mp4"
video_bitrate_str = "3000k"
buffer_size_str = "6000k"
audio_bitrate_str = "128k"

# specific config class to match your snippet structure
class StreamConfig:
    resolution = "1920x1080" # Change to 1280x720 if you want lower usage
    frame_rate = 30
    audio_sample_rate = 44100

stream_config = StreamConfig()

# --- YOUR COMMAND ---
ffmpeg_cmd = [
    'ffmpeg',
    '-re',                       # Read input at native frame rate
    '-stream_loop', '-1',        # Loop input infinitely
    '-i', video_path,
    
    # --- VIDEO OPTIMIZATIONS ---
    '-c:v', 'libx264',
    '-preset', 'ultrafast',      # Changed to ultrafast for speed
    '-tune', 'zerolatency',      # essential for live streaming
    '-threads', '0',             # Use all CPU cores
    
    # Bitrate Control
    '-b:v', video_bitrate_str,
    '-maxrate', video_bitrate_str,   # Cap maxrate equal to bitrate for stability
    '-bufsize', buffer_size_str,     # Buffer size
    
    # Video Format
    '-vf', f'scale={stream_config.resolution}',
    '-r', str(stream_config.frame_rate),
    '-pix_fmt', 'yuv420p',
    '-g', '60',                  # Force keyframe every 2s (assuming 30fps)
    
    # --- AUDIO SETTINGS ---
    '-c:a', 'aac',
    '-b:a', audio_bitrate_str,
    '-ar', str(stream_config.audio_sample_rate),
    
    # --- OUTPUT ---
    '-f', 'flv',
    rtmp_url
]

print("Starting Stream with command:")
print(" ".join(ffmpeg_cmd))

# Run the command
try:
    subprocess.run(ffmpeg_cmd, check=True)
except KeyboardInterrupt:
    print("Stream stopped by user.")
except Exception as e:
    print(f"Error occurred: {e}")
