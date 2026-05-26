import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from moviepy import *
import edge_tts
import asyncio
import os
import tempfile
import uuid

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="ANDROIDETV AI DUBBING PRO",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 ANDROIDETV AI DUBBING PRO")
st.subheader("🔥 Doblaje IA Profesional")

# ======================================================
# IDIOMAS
# ======================================================

idiomas = {
    "🇺🇸 Inglés": "en",
    "🇪🇸 Español": "es",
    "🇫🇷 Francés": "fr",
    "🇩🇪 Alemán": "de",
    "🇮🇹 Italiano": "it",
    "🇵🇹 Portugués": "pt",
    "🇯🇵 Japonés": "ja",
    "🇰🇷 Coreano": "ko",
    "🇨🇳 Chino": "zh-cn",
    "🇸🇦 Árabe": "ar",
    "🇮🇳 Hindi": "hi"
}

# ======================================================
# VOCES
# ======================================================

voces = {

    "🔥 Hombre Español":
    "es-ES-AlvaroNeural",

    "🔥 Mujer Español":
    "es-ES-ElviraNeural",

    "🔥 Hombre Inglés":
    "en-US-GuyNeural",

    "🔥 Mujer Inglés":
    "en-US-JennyNeural",

    "🔥 Hombre Francés":
    "fr-FR-HenriNeural",

    "🔥 Mujer Francesa":
    "fr-FR-DeniseNeural"
}

# ======================================================
# SUBIR VIDEO
# ======================================================

uploaded_file = st.file_uploader(
    "📤 Sube tu video",
    type=["mp4", "mov", "avi", "mkv"]
)

# ======================================================
# OPCIONES
# ======================================================

col1, col2 = st.columns(2)

with col1:

    idioma_nombre = st.selectbox(
        "🌍 Idioma destino",
        list(idiomas.keys())
    )

with col2:

    voz_nombre = st.selectbox(
        "🎙️ Voz IA",
        list(voces.keys())
    )

target_lang = idiomas[idioma_nombre]
voz = voces[voz_nombre]

# ======================================================
# OPCIONES PRO
# ======================================================

mantener_original = st.checkbox(
    "🎧 Mantener voz original",
    value=True
)

volumen_original = st.slider(
    "🔉 Volumen voz original",
    0.0,
    1.0,
    0.20
)

velocidad_voz = st.slider(
    "⚡ Velocidad IA",
    -50,
    50,
    -5
)

# ======================================================
# GENERAR AUDIO
# ======================================================

async def generar_audio(texto, voz, salida, velocidad):

    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate=f"{velocidad}%"
    )

    await communicate.save(salida)

# ======================================================
# PROCESAR VIDEO
# ======================================================

if uploaded_file is not None:

    st.video(uploaded_file)

    if st.button("🚀 GENERAR DOBLAJE"):

        try:

            temp_dir = tempfile.mkdtemp()

            video_path = os.path.join(
                temp_dir,
                f"{uuid.uuid4()}.mp4"
            )

            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            # ==================================================
            # EXTRAER AUDIO
            # ==================================================

            st.info("🎧 Extrayendo audio...")

            video = VideoFileClip(video_path)

            audio_path = os.path.join(
                temp_dir,
                "audio.wav"
            )

            video.audio.write_audiofile(audio_path)

            # ==================================================
            # TRANSCRIBIR
            # ==================================================

            st.info("🧠 Transcribiendo IA...")

            model = whisper.load_model("base")

            result = model.transcribe(audio_path)

            texto_original = result["text"]

            st.success("✅ Texto detectado")

            # ==================================================
            # TRADUCIR
            # ==================================================

            st.info("🌍 Traduciendo...")

            texto_traducido = GoogleTranslator(
                source="auto",
                target=target_lang
            ).translate(texto_original)

            st.success("✅ Traducción lista")

            # ==================================================
            # GENERAR VOZ IA
            # ==================================================

            st.info("🎙️ Generando voz IA...")

            voz_generada = os.path.join(
                temp_dir,
                "voz.mp3"
            )

            asyncio.run(
                generar_audio(
                    texto_traducido,
                    voz,
                    voz_generada,
                    velocidad_voz
                )
            )

            # ==================================================
            # CREAR VIDEO FINAL
            # ==================================================

            st.info("🎬 Renderizando video...")

            audio_ia = AudioFileClip(
                voz_generada
            )

            if mantener_original:

                audio_original = video.audio.volumex(
                    volumen_original
                )

                final_audio = CompositeAudioClip([
                    audio_original,
                    audio_ia
                ])

            else:

                final_audio = audio_ia

            final_video = video.set_audio(
                final_audio
            )

            output_path = os.path.join(
                temp_dir,
                "doblado.mp4"
            )

            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=4
            )

            st.success("🎉 VIDEO COMPLETADO")

            st.video(output_path)

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇️ DESCARGAR VIDEO",
                    file,
                    file_name="ANDROIDETV_DOBLADO.mp4",
                    mime="video/mp4"
                )

        except Exception as e:

            st.error(f"❌ ERROR: {e}")
