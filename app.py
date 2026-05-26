import streamlit as st
import moviepy.editor as mp
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

st.title("🎬 Automatic Video Dubbing - Androidetv")

video_file = st.file_uploader("Upload your video to process", type=['mp4', 'mov', 'avi'])
idioma = st.selectbox("Select target language", ["en", "fr", "pt", "de", "it"])

if video_file and st.button("Start Dubbing"):
    with st.spinner("Processing... this may take a few minutes."):
        with open("temp_video.mp4", "wb") as f:
            f.write(video_file.read())

        model = whisper.load_model("base")
        result = model.transcribe("temp_video.mp4")
        
        translation = GoogleTranslator(source='auto', target=idioma).translate(result['text'])
        
        tts = gTTS(translation, lang=idioma)
        tts.save("temp_audio.mp3")
        
        video = mp.VideoFileClip("temp_video.mp4")
        nuevo_audio = mp.AudioFileClip("temp_audio.mp3")
        final_video = video.set_audio(nuevo_audio)
        final_video.write_videofile("video_doblado.mp4", codec="libx264")
        
        st.video("video_doblado.mp4")
        with open("video_doblado.mp4", "rb") as file:
            st.download_button("Download Dubbed Video", file, "video_listo.mp4")
