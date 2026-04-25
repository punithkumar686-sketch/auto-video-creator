from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
import os

def create_video(mode="mobile"):

    BASE_DIR = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))

    bg_path = os.path.join(root_dir, "assets", "bg.mp4")
    music_path = os.path.join(root_dir, "assets", "music.mp3")
    output_dir = os.path.join(root_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    # 📱 / 🖥 resolution
    if mode == "mobile":
        W, H = 1080, 1920
        filename = "mobile_video.mp4"
        fontsize = 70
    else:
        W, H = 1920, 1080
        filename = "desktop_video.mp4"
        fontsize = 60

    # 🎬 Load background video
    bg = VideoFileClip(bg_path).resize((W, H))

    # 🎵 Background music
    audio = AudioFileClip(music_path)

    # 🎯 SCREEN CONTENT + TIMING
    screens = [
        ("Can you solve this in 3 seconds?\nMost kids can’t!", 2.5),
        ("Try this:\n47 + 25", 2.5),
        ("Instead of adding normally…\nAdd 50 + 25 = 75", 3),
        ("Then subtract 3 → 72\nBoom! Faster than your teacher!\n\nFollow for more brain tricks!", 4),
    ]

    clips = []
    start = 0

    for text, duration in screens:

        subclip = bg.subclip(start, start + duration)

        txt = TextClip(
            text,
            fontsize=fontsize,
            color="white",
            method="caption",
            size=(int(W * 0.8), None),  # safe margins
            align="center"
        ).set_position(("center", "center")).set_duration(duration)

        final = CompositeVideoClip([subclip, txt])
        clips.append(final)

        start += duration

    final_video = concatenate_videoclips(clips)

    # 🎵 LOOP MUSIC TO MATCH VIDEO LENGTH
    final_audio = audio.audio_loop(duration=final_video.duration)

    final_video = final_video.set_audio(final_audio)

    output_path = os.path.join(output_dir, filename)

    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path
