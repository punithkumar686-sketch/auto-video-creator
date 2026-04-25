from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_screen(text, size, font_size, duration):

    img = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 🧠 Center text properly
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (size[0] - text_w) / 2
    y = (size[1] - text_h) / 2

    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255),
        align="center",
        spacing=15
    )

    path = f"temp_{hash(text)}.png"
    img.save(path)

    return ImageClip(path).set_duration(duration)


def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 📱 MOBILE / 🖥 DESKTOP
    if mode == "mobile":
        size = (1080, 1920)
        font_size = 70
        video_name = "mobile_video.mp4"
    else:
        size = (1920, 1080)
        font_size = 55
        video_name = "desktop_video.mp4"

    # 🎬 SCREEN CONTENT (YOUR VIRAL STRUCTURE)
    screens = [

        # SCREEN 1 - HOOK
        ("Can you solve this in 3 seconds?\nMost kids can’t!", 3),

        # SCREEN 2 - QUESTION
        ("Try this:\n47 + 25", 3),

        # SCREEN 3 - TRICK STEP
        ("Instead of adding normally…\nAdd 50 + 25 = 75", 3),
        ("Taking time to add right", 3),

        # SCREEN 4 - FINAL ANSWER + CTA
        ("Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!", 4),
    ]

    clips = []

    for text, duration in screens:
        clip = create_screen(text, size, font_size, duration)
        clips.append(clip)

    # 🎞 Combine screens
    final_clip = concatenate_videoclips(clips, method="compose")

    # 🎥 Output path
    video_path = os.path.join(output_dir, video_name)

    # 🔊 Add audio if exists
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(audio)

    # 🚀 EXPORT VIDEO
    final_clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    # 🧹 Cleanup temp images
    final_clip.close()

    return video_path
