from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 📱 MOBILE vs 🖥 DESKTOP SETTINGS
    if mode == "mobile":
        W, H = 1080, 1920
        font_size = 65
        video_name = "mobile_video.mp4"
        duration = 10
    else:
        W, H = 1920, 1080
        font_size = 55
        video_name = "desktop_video.mp4"
        duration = 10

    # 🎬 BACKGROUND
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 🔤 FONT
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 🧠 VIRAL STRUCTURE
    content = f"""
⏱ 3 SECOND CHALLENGE

{text}
"""

    # 📐 PERFECT CENTER ALIGNMENT LOGIC
    bbox = draw.multiline_textbbox((0, 0), content, font=font, align="center")

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (W - text_width) / 2
    y = (H - text_height) / 2

    # ✍️ DRAW TEXT (CENTERED PERFECTLY)
    draw.multiline_text(
        (x, y),
        content,
        font=font,
        fill=(255, 255, 255),
        align="center",
        spacing=15
    )

    # 💾 SAVE FRAME
    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    # 🎥 OUTPUT VIDEO
    video_path = os.path.join(output_dir, video_name)

    clip = ImageClip(img_path).set_duration(duration)

    # 🔊 AUDIO
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    # 🚀 EXPORT (OPTIMIZED FOR VIRAL SHORTS)
    clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return video_path
