from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import os

def create_video(text, audio_path=None, mode="mobile"):

    # 📁 PATH SETUP
    BASE_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

    output_dir = os.path.join(ROOT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    bg_video_path = os.path.join(ROOT_DIR, "assets", "background.mp4")

    # ❌ Safety check
    if not os.path.exists(bg_video_path):
        raise FileNotFoundError(f"Background video not found at: {bg_video_path}")

    # 🎬 Load background
    bg = VideoFileClip(bg_video_path)

    # 📱 / 🖥 Resolution
    if mode == "mobile":
        W, H = 1080, 1920
        font_size = 70
        filename = "mobile_video.mp4"
    else:
        W, H = 1920, 1080
        font_size = 60
        filename = "desktop_video.mp4"

    bg = bg.resize((W, H))

    # 🎯 Screens (viral structure)
    screens = [
        ("Can you solve this in 3 seconds?\nMost kids can’t!", 2.5),
        ("Try this:\n47 + 25", 2.5),
        ("Instead of adding normally…\nAdd 50 + 25 = 75", 3),
        ("Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!", 4),
    ]

    clips = []
    start = 0

    # 🎬 Create each screen
    for screen_text, duration in screens:

        end = start + duration

        # Loop background if shorter than needed
        if end > bg.duration:
            sub_bg = bg.loop(duration=duration)
        else:
            sub_bg = bg.subclip(start, end)

        # 🧠 TEXT (NO font= → avoids ImageMagick error)
        txt = TextClip(
            screen_text,
            fontsize=font_size,
            color="white",
            method="caption",  # SAFE MODE
            size=(int(W * 0.8), None),
            align="center"
        )

        txt = txt.set_position(("center", "center")).set_duration(duration)

        video = CompositeVideoClip([sub_bg, txt])
        clips.append(video)

        start += duration

    # 🎞 Merge clips
    final_video = concatenate_videoclips(clips, method="compose")

    # 🔊 Add audio (optional)
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)

        # Match audio length to video
        if audio.duration < final_video.duration:
            audio = audio.audio_loop(duration=final_video.duration)
        else:
            audio = audio.subclip(0, final_video.duration)

        final_video = final_video.set_audio(audio)

    # 🎥 Export
    video_path = os.path.join(output_dir, filename)

    final_video.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return video_path
