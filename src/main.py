import os

os.makedirs("output", exist_ok=True)

from ai_script import generate_script
from video import create_video
from voice import generate_voice

def main():

    # 1. Viral script
    script = generate_script()
    print("SCRIPT:\n", script)

    # 2. Voice
    audio = generate_voice(script)

    # 3. Video
    video_path = create_video(script, audio)

    print("VIDEO READY:", video_path)

if __name__ == "__main__":
    main()
