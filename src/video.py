from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None):
    # Absolute safe output folder
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create image (vertical video format)
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Font fallback
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Draw text (basic centering)
    draw.multiline_text(
        (100, 800),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # Save frame
    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    # Create video
    video_path = os.path.join(output_dir, "video.mp4")
    clip = ImageClip(img_path).set_duration(10)

    # Add audio if exists
    if audio_path:
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    clip.write_videofile(video_path, fps=24)

    # Cleanup (VERY IMPORTANT for GitHub Actions)
    clip.close()
    if audio_path:
        audio.close()

    return video_path
