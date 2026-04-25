from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip
)
from PIL import Image, ImageDraw, ImageFont
import os

# 🎨 TEXT IMAGE
def create_text_image(text, size, font_size):

    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    color = (255, 255, 0) if any(c.isdigit() for c in text) else (255, 255, 255)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (size[0] - w) // 2
    y = (size[1] - h) // 2

    draw.text((x, y), text, font=font, fill=color)

    path = f"/tmp/{abs(hash(text))}.png"
    img.save(path)

    return path


# 🎬 WORD ANIMATION
def animate_lines(lines, size, font_size):

    clips = []
    t = 0

    for line in lines:
        img = create_text_image(line, size, font_size)

        clip = (
            ImageClip(img)
            .set_start(t)
            .set_duration(1.2)
            .fadein(0.3)
            .fadeout(0.3)
            .set_position("center")
        )

        clips.append(clip)
        t += 1.2

    return clips, t


# ⏱ COUNTDOWN SOUND
def create_beep():

    from moviepy.audio.AudioClip import AudioClip
    import numpy as np

    def make_sound(t):
        return 0.5 * np.sin(440 * 2 * np.pi * t)

    return AudioClip(make_sound, duration=0.3)


# 🎬 MAIN VIDEO
def create_video(text, voice_path=None, mode="mobile"):

    BASE = os.path.dirname(__file__)
    ROOT = os.path.abspath(os.path.join(BASE, ".."))

    bg_path = os.path.join(ROOT, "assets", "background.mp4")
    music_path = os.path.join(ROOT, "assets", "music.mp3")

    output_dir = os.path.join(ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    bg = VideoFileClip(bg_path)

    if mode == "mobile":
        W, H = 1080, 1920
        font_size = 70
        filename = f"mobile_{os.getpid()}.mp4"
    else:
        W, H = 1920, 1080
        font_size = 60
        filename = f"desktop_{os.getpid()}.mp4"

    bg = bg.resize((W, H))

    # 🎯 SCREENS
    screens = [
        ["Can you solve this", "in 3 seconds?", "Most kids can’t!"],
        ["Try this:"],
        ["47 + 25"],
        ["Add 50 + 25 = 75"],
        ["Then subtract 3 → 72"],
        ["Boom! Faster than your teacher!"],
        ["Follow for more brain tricks!"]
    ]

    clips = []
    start = 0

    for lines in screens:

        text_clips, duration = animate_lines(lines, (W, H), font_size)

        if start + duration > bg.duration:
            sub_bg = bg.loop(duration=duration)
        else:
            sub_bg = bg.subclip(start, start + duration)

        # 🔥 zoom effect
        sub_bg = sub_bg.resize(lambda t: 1 + 0.03 * t)

        video = CompositeVideoClip([sub_bg] + text_clips)
        clips.append(video)

        start += duration

    final = concatenate_videoclips(clips)

    # 🔊 VOICE
    if voice_path and os.path.exists(voice_path):
        voice = AudioFileClip(voice_path)
        voice = voice.volumex(1.2)
        final = final.set_audio(voice)

    # 🔊 BACKGROUND MUSIC
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.2)

        if final.audio:
            final.audio = final.audio.audio_loop(duration=final.duration)
            final = final.set_audio(final.audio.volumex(1).fx(
                lambda a: a
            ))
        else:
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
