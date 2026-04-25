import os

from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip
)
from PIL import Image, ImageDraw, ImageFont

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

    # 🔊 LOAD VOICE FIRST (CRITICAL FOR SYNC)
    audio = None
    if voice_path and os.path.exists(voice_path):
        audio = AudioFileClip(voice_path)
        total_audio_duration = audio.duration
    else:
        total_audio_duration = len(screens) * 2  # fallback

    # 🎯 DISTRIBUTE TIME PROPERLY
    per_screen_duration = total_audio_duration / len(screens)

    clips = []
    start = 0

    for lines in screens:

        # ✅ PASS DURATION HERE (THIS FIXES EVERYTHING)
        text_clips, duration = animate_lines(
            lines, (W, H), font_size, per_screen_duration
        )

        if start + duration > bg.duration:
            sub_bg = bg.loop(duration=duration)
        else:
            sub_bg = bg.subclip(start, start + duration)

        # 🔥 Smooth zoom
        sub_bg = sub_bg.resize(lambda t: 1 + 0.02 * t)

        video = CompositeVideoClip([sub_bg] + text_clips)
        clips.append(video)

        start += duration

    final = concatenate_videoclips(clips, method="compose")

    # 🔊 PERFECT AUDIO SYNC
    if audio:
        audio = audio.set_duration(final.duration)
        final = final.set_audio(audio)

    # 🔊 BACKGROUND MUSIC (LOW VOLUME)
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.15)

        if audio:
            # mix voice + music
            from moviepy.audio.AudioClip import CompositeAudioClip

            music = music.audio_loop(duration=final.duration)
            final_audio = CompositeAudioClip([audio, music])
            final = final.set_audio(final_audio)
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
