from ai_script import generate_script
from video import create_video

def main():
    script = generate_script()
    print(script)
    create_video(script)

if __name__ == "__main__":
    main()
