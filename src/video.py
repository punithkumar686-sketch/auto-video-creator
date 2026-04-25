import os
import time

from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip
)

from PIL import Image, ImageDraw, ImageFont


# 🎨 CREATE WORD IMAGE
def create_word_image(word, size, font_size):

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # 🎯 highlight numbers
    color = (255, 255, 0) if any(c.isdigit() for c in word) else (255, 255, 255)

    bbox = draw.textbbox((0, 0), word, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (size[0] - w) // 2
    y = (size[1] - h) // 2

    draw.text((x, y), word, font=font, fill=color)

    path = f"/tmp/{abs(hash(word + str(time.time())))}.png"
    img.save(path)

    return path


# 🎬 WORD-BY-WORD ANIMATION
def animate_words(sentence, size, font_size, duration):

    words = sentence.split()
    clips = []

    t = 0
    per_word = duration / max(len(words), 1)

    for word in words:
        img = create_word_image(word, size, font_size)

        clip = (
            ImageClip(img)
            .set_start(t)
            .set_duration(per_word)
            .fadein(0.15)
            .fadeout(0.15)
            .set_position("center")
        )

        clips.append(clip)
        t += per_word

    return clips


# 🎬 MAIN VIDEO
def create_video(text, voice_path=None, mode="mobile"):

    BASE = os.path.dirname(__file__)
    ROOT = os.path.abspath(os.path.join(BASE, ".."))

    bg_path = os.path.join(ROOT, "assets", "background.mp4")
    music_path = os.path.join(ROOT, "assets", "music.mp3")

    output_dir = os.path.join(ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"Missing background video: {bg_path}")

    bg = VideoFileClip(bg_path)

    if mode == "mobile":
        W, H = 1080, 1920
        font_size = 75
        filename = f"mobile_{int(time.time()*1000)}.mp4"
    else:
        W, H = 1920, 1080
        font_size = 65
        filename = f"desktop_{int(time.time()*1000)}.mp4"

    bg = bg.resize((W, H))

    # 🎯 SPLIT SCRIPT INTO LINES
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    total_duration = len(lines) * 1.8
    per_line_duration = total_duration / len(lines)

    clips = []
    start = 0

    for line in lines:

        # 🎬 animate words
        text_clips = animate_words(
            line, (W, H), font_size, per_line_duration
        )

        if start + per_line_duration > bg.duration:
            sub_bg = bg.loop(duration=per_line_duration)
        else:
            sub_bg = bg.subclip(start, start + per_line_duration)

        # 🔥 smooth zoom
        sub_bg = sub_bg.resize(lambda t: 1 + 0.02 * t)

        video = CompositeVideoClip([sub_bg] + text_clips)
        video = video.set_duration(per_line_duration)

        clips.append(video)
        start += per_line_duration

    final = concatenate_videoclips(clips, method="compose")

    # 🔊 BACKGROUND MUSIC ONLY
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.2)
        music = music.audio_loop(duration=final.duration)
        final = final.set_audio(music)

    output = os.path.join(output_dir, filename)

    final.write_videofile(
        output,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output
