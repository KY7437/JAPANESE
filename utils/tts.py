from TTS.api import TTS
import streamlit as st

@st.cache_resource
def load_tts():
    return TTS(model_name="tts_models/ja/kokoro/tacotron2-DDC")

def generate_tts(text, path):
    tts = load_tts()
    tts.tts_to_file(text=text, file_path=path)
