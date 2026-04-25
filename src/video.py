from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import os

# 🎨 Create text image
def create_text_image(text, size, font_size):

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    max_width = int(size[0] * 0.8)

    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = line + word + " "
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w < max_width:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    final_text = "\n".join(lines)

    bbox = draw.multiline_textbbox((0, 0), final_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (size[0] - text_w) // 2
    y = (size[1] - text_h) // 2

    draw.multiline_text(
        (x, y),
        final_text,
        font=font,
        fill=(255, 255, 255),
        align="center",
        spacing=10
    )

    path = f"/tmp/text_{abs(hash(text))}.png"
    img.save(path)

    return path


# ⏱ Countdown animation
def create_countdown(size, duration=3):

    clips = []
    for i in range(3, 0, -1):
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 200)
        except:
            font = ImageFont.load_default()

        text = str(i)

        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        x = (size[0] - w) // 2
        y = (size[1] - h) // 2

        draw.text((x, y), text, font=font, fill=(255, 0, 0))

        path = f"/tmp/count_{i}.png"
        img.save(path)

        clip = ImageClip(path).set_duration(1).fadein(0.3).fadeout(0.3)
        clips.append(clip)

    return concatenate_videoclips(clips)


def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

    output_dir = os.path.join(ROOT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    bg_path = os.path.join(ROOT_DIR, "assets", "background.mp4")

    if not os.path.exists(bg_path):
        raise FileNotFoundError("Background video missing")

    bg = VideoFileClip(bg_path)

    # 📱 / 🖥 resolution
    if mode == "mobile":
        W, H = 1080, 1920
        font_size = 70
        filename = "mobile_video.mp4"
    else:
        W, H = 1920, 1080
        font_size = 60
        filename = "desktop_video.mp4"

    bg = bg.resize((W, H))

    # 🎬 Screens
    screens = [
        ("Can you solve this in 3 seconds?\nMost kids can’t!", 2.5),
        ("Try this:\n47 + 25", 2.5),
        ("Instead of adding normally…\nAdd 50 + 25 = 75", 3),
        ("Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!", 4),
    ]

    clips = []
    start = 0

    # ⏱ Add countdown FIRST
    countdown = create_countdown((W, H))
    clips.append(countdown)

    for screen_text, duration in screens:

        end = start + duration

        if end > bg.duration:
            sub_bg = bg.loop(duration=duration)
        else:
            sub_bg = bg.subclip(start, end)

        text_img = create_text_image(screen_text, (W, H), font_size)

        txt_clip = ImageClip(text_img).set_duration(duration).fadein(0.5)

        video = CompositeVideoClip([
            sub_bg.fadein(0.5),
            txt_clip.set_position("center")
        ])

        clips.append(video)
        start += duration

    final = concatenate_videoclips(clips, method="compose")

    # 🔊 Audio
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)

        if audio.duration < final.duration:
            audio = audio.audio_loop(duration=final.duration)
        else:
            audio = audio.subclip(0, final.duration)

        final = final.set_audio(audio)

    output_path = os.path.join(output_dir, filename)

    final.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path
