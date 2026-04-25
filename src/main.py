from ai_script import generate_script
from video import create_video
from voice import generate_voice

def main():

    script = generate_script()
    print("SCRIPT:\n", script)

    voice = generate_voice(script)

    create_video(script, voice, "mobile")
    create_video(script, voice, "desktop")

if __name__ == "__main__":
    main()
