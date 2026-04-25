from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None):
    # Output folder
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Create vertical image (1080x1920)
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Font fallback
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Draw text
    draw.multiline_text(
        (100, 800),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # Save image frame
    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    # Create video path
    video_path = os.path.join(output_dir, "video.mp4")

    # Create clip
    clip = ImageClip(img_path).set_duration(10)

    # Add audio if exists
    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    # 🔥 FIXED EXPORT (IMPORTANT)
    clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    # Cleanup
    clip.close()
    if audio:
        audio.close()

    print("Video saved at:", video_path)
    print("Output files:", os.listdir(output_dir))

    return video_path
