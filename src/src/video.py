from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_video(text, audio_path):
    os.makedirs("../output", exist_ok=True)

    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    draw.multiline_text((100, 800), text, font=font, fill=(255,255,255))

    img_path = "../output/frame.png"
    img.save(img_path)

    video_path = "../output/video.mp4"

    clip = ImageClip(img_path).set_duration(10)
    audio = AudioFileClip(audio_path)

    clip = clip.set_audio(audio)

    clip.write_videofile(video_path, fps=24)

    return video_path
