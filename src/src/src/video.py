from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

def create_video(text):
    # Create image with text
    img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    draw.text((100, 800), text, font=font, fill=(255, 255, 255))

    img.save("output/frame.png")

    # Convert image to video
    clip = ImageClip("output/frame.png").set_duration(10)
    clip.write_videofile("output/video.mp4", fps=24)
