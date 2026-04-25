from gtts import gTTS
import os

def generate_voice(text):
    output_dir = os.path.join("output")
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "audio.mp3")

    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(audio_path)

    return audio_path
