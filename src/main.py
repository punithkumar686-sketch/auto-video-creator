from ai_script import generate_script
from video import create_video
from voice import generate_voice

def main():
    script = generate_script()
    print("Script:", script)

    audio = generate_voice(script)

    video = create_video(script, audio)

    print("Video created:", video)

if __name__ == "__main__":
    main()
