from ai_script import generate_script
from voice import generate_voice
from video import create_video

def main():

    script = generate_script()
    print("SCRIPT GENERATED:\n", script)

    audio = generate_voice(script)

    # 📱 MOBILE VIRAL SHORTS
    mobile_video = create_video(script, audio, mode="mobile")
    print("Mobile video:", mobile_video)

    # 🖥 DESKTOP VERSION
    desktop_video = create_video(script, audio, mode="desktop")
    print("Desktop video:", desktop_video)

if __name__ == "__main__":
    main()
