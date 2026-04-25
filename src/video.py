from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 🧠 Choose resolution based on mode
    if mode == "mobile":
        size = (1080, 1920)   # Shorts
        filename = "video_mobile.mp4"
        font_size = 65
        position = (80, 600)

    else:
        size = (1920, 1080)   # Desktop
        filename = "video_desktop.mp4"
        font_size = 50
        position = (200, 400)

    # 🎬 Create background
    img = Image.new('RGB', size, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 🔤 Font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 📝 Format text
    formatted_text = f"""
⏱ 3 SECOND CHALLENGE

{text}
"""

    draw.multiline_text(
        position,
        formatted_text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # 💾 Save frame
    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    # 🎥 Video path
    video_path = os.path.join(output_dir, filename)

    # 🎞 Create clip
    clip = ImageClip(img_path).set_duration(10)

    # 🔊 Audio
    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    # 🚀 Export video
    clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return video_path
