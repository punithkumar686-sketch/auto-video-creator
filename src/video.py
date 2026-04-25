from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text):
    # Ensure output folder exists
    os.makedirs("../output", exist_ok=True)

    # Create image (black background)
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try to use a good font, fallback if not available
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Add text to image
    draw.multiline_text(
        (100, 800),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # Save image
    img_path = "../output/frame.png"
    img.save(img_path)

    # Convert image to video
    video_path = "../output/video.mp4"
    clip = ImageClip(img_path).set_duration(10)
    clip.write_videofile(video_path, fps=24)

    return video_path
