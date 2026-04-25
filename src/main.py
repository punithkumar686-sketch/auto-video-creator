from ai_script import generate_script
from video import create_video
from metadata import generate_metadata
import os

def main():

    script = generate_script()
    print("SCRIPT GENERATED:\n", script)

    # 🎬 Create videos
    mobile_video = create_video(script, None, mode="mobile")
    desktop_video = create_video(script, None, mode="desktop")

    # 🧠 Metadata
    meta = generate_metadata()

    # 💾 Save metadata
    output_path = os.path.join("..", "output", "metadata.txt")

    with open(output_path, "w") as f:
        f.write(f"Title: {meta['title']}\n")
        f.write(f"Hashtags: {meta['hashtags']}\n")

    print("VIDEOS CREATED:")
    print(mobile_video)
    print(desktop_video)
    print("METADATA SAVED")

if __name__ == "__main__":
    main()
