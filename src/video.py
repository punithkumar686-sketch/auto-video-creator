from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

def create_screen(text, size, font, duration, bg_color):

    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    # Safe margin (important for mobile)
    margin_x = int(size[0] * 0.1)
    margin_y = int(size[1] * 0.2)

    max_width = size[0] - 2 * margin_x

    # Wrap text manually (important)
    lines = []
    words = text.split()
    line = ""

    for word in words:
        test = line + word + " "
        w = draw.textbbox((0,0), test, font=font)[2]
        if w < max_width:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    final_text = "\n".join(lines)

    bbox = draw.multiline_textbbox((0,0), final_text, font=font, align="center")

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (size[0] - text_w) / 2
    y = (size[1] - text_h) / 2

    draw.multiline_text(
        (x, y),
        final_text,
        font=font,
        fill=(255,255,255),
        align="center",
        spacing=12
    )

    path = f"temp_{hash(text)}.png"
    img.save(path)

    return ImageClip(path).set_duration(duration)


def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 📱 / 🖥 settings
    if mode == "mobile":
        size = (1080, 1920)
        font_size = 70
        filename = "mobile_video.mp4"
    else:
        size = (1920, 1080)
        font_size = 55
        filename = "desktop_video.mp4"

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 🎨 Background colors (acts like different scenes)
    backgrounds = [
        (20, 20, 20),
        (30, 30, 60),
        (60, 30, 30),
        (20, 50, 20)
    ]

    # 🎬 Screens
    screens = [
        "Can you solve this in 3 seconds?\nMost kids can’t!",
        "Try this:\n47 + 25",
        "Instead of adding normally…\nAdd 50 + 25 = 75",
        "Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!"
    ]

    clips = []

    # 🔊 AUDIO SYNC FIX
    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
    else:
        total_duration = 12  # fallback

    per_screen_duration = total_duration / len(screens)

    # 🎬 Create clips
    for i, text in enumerate(screens):
        clip = create_screen(
            text,
            size,
            font,
            per_screen_duration,
            backgrounds[i % len(backgrounds)]
        )
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")

    if audio:
        final_clip = final_clip.set_audio(audio)

    video_path = os.path.join(output_dir, filename)

    final_clip.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    final_clip.close()

    return video_path
