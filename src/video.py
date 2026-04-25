from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path=None):

    # 🔥 FIXED OUTPUT PATH (GitHub + Local safe)
    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 🎬 Create vertical background (Shorts format)
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 🔤 Font setup
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()

    # 📝 Draw text (center style)
    draw.multiline_text(
        (100, 800),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center"
    )

    # 💾 Save frame image
    img_path = os.path.join(output_dir, "frame.png")
    img.save(img_path)

    # 🎥 Output video file
    video_path = os.path.join(output_dir, "video.mp4")

    # 🎞 Create clip
    clip = ImageClip(img_path).set_duration(10)

    # 🔊 Add audio if available
    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

    # 🚀 EXPORT VIDEO (CRITICAL FIX FOR GITHUB ACTIONS)
    clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="ultrafast",
        verbose=False,
        logger=None
    )

    # 🧹 Cleanup memory
    clip.close()
    if audio:
        audio.close()

    print("✅ Video created successfully:", video_path)
    print("📁 Output folder contents:", os.listdir(output_dir))

    return video_path
