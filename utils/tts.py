from gtts import gTTS

def generate_tts(text, path):
    tts = gTTS(text=text, lang="ja")
    tts.save(path)
