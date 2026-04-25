from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # Background
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()

    # VIRAL TEXT FORMAT (centered + bold look)
    wrapped_text = text.upper()

    draw.multiline_text(
        (80, 700),
        wrapped_text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    video_path = os.path.join(output_dir, "video.mp4")

    clip = ImageClip(img_path).set_duration(10)

    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    # 🔥 VIRAL EXPORT SETTINGS
    clip.write_videofile(
        video_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4,
        logger=None
    )

    clip.close()
    if audio:
        audio.close()

    return video_path
