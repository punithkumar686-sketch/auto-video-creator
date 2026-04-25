from ai_script import generate_script
from video import create_video

def main():

    script = generate_script()
    print("SCRIPT:\n", script)

    create_video(script, None, "mobile")
    create_video(script, None, "desktop")

if __name__ == "__main__":
    main()
