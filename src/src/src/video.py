from moviepy.editor import *

def create_video(text):
    bg = ColorClip(size=(1080,1920), color=(0,0,0), duration=10)

    txt = TextClip(
        text,
        fontsize=80,
        color='white',
        method='caption',
        size=(900,1600)
    ).set_position("center").set_duration(10)

    final = CompositeVideoClip([bg, txt])

    final.write_videofile("output/video.mp4", fps=24)
