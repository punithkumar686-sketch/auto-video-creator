from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import os

def create_video(text, audio_path=None, mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    output_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
    os.makedirs(output_dir, exist_ok=True)

    # 📁 Background video (PUT FILE HERE)
    bg_video_path = os.path.join(BASE_DIR, "background.mp4")

    bg = VideoFileClip(bg_video_path).loop(duration=20)

    # 📱 / 🖥 Resolution
    if mode == "mobile":
        bg = bg.resize((1080, 1920))
        font_size = 70
        filename = "mobile_video.mp4"
    else:
        bg = bg.resize((1920, 1080))
        font_size = 60
        filename = "desktop_video.mp4"

    # 🎬 SCREENS
    screens = [
        "Can you solve this in 3 seconds?\nMost kids can’t!",
        "Try this:\n47 + 25",
        "Instead of adding normally…\nAdd 50 + 25 = 75",
        "Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!"
    ]

    # 🔊 AUDIO SPLIT FIX
    audio = None
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
    else:
        total_duration = 12

    per_duration = total_duration / len(screens)

    clips = []

    for i, screen_text in enumerate(screens):

        start = i * per_duration
        end = start + per_duration

        # 🎯 CUT AUDIO PER SCREEN
        sub_audio = None
        if audio:
            sub_audio = audio.subclip(start, end)

        # 🧠 TEXT DESIGN (VISIBLE ON VIDEO)
        txt = TextClip(
            screen_text,
            fontsize=font_size,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(bg.w * 0.8, None),
            align="center"
        )

        txt = txt.set_position(("center", "center")).set_duration(per_duration)

        # 🔥 OVERLAY TEXT ON VIDEO
        video = CompositeVideoClip([bg.subclip(start, end), txt])

        if sub_audio:
            video = video.set_audio(sub_audio)

        clips.append(video)

    final = concatenate_videoclips(clips)

    video_path = os.path.join(output_dir, filename)

    final.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return video_path
