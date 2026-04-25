from gtts import gTTS
import os

def generate_voice(text):

    output_path = "/tmp/voice.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(output_path)

    return output_path
