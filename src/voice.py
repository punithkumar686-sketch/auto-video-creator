from gtts import gTTS
import os

def generate_voice(text):
    os.makedirs("../output", exist_ok=True)
    file_path = "../output/voice.mp3"

    tts = gTTS(text=text, lang='en')
    tts.save(file_path)

    return file_path
