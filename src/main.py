import os

# ensure root output folder exists
os.makedirs("output", exist_ok=True)

from ai_script import generate_script
from video import create_video
from voice import generate_voice

def main():
    script = generate_script()
    print("📝 Script:", script)

    audio = generate_voice(script)
    print("🔊 Audio created:", audio)

    video_path = create_video(script, audio)

    print("🎬 Video created at:", video_path)

if __name__ == "__main__":
    main()
