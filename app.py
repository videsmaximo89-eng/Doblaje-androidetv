import streamlit as st
import whisper
from deep_translator import GoogleTranslator

from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import CompositeAudioClip

import edge_tts
import asyncio
import os
import tempfile
import uuid

from pydub import AudioSegment
from pydub.effects import normalize

# ======================================================
# CONFIGURACIÓN GENERAL
# ======================================================

st.set_page_config(
    page_title="ANDROIDETV AI DUBBING PRO MAX",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 ANDROIDETV AI DUBBING PRO MAX")
st.subheader("🔥 Doblaje IA profesional con voz original")

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
    "🇮🇳 Hindi": "hi",
    "🇷🇺 Ruso": "ru",
    "🇹🇷 Turco": "tr",
    "🇳🇱 Holandés": "nl",
    "🇵🇱 Polaco": "pl",
    "🇸🇪 Sueco": "sv",
    "🇫🇮 Finlandés": "fi",
    "🇬🇷 Griego": "el",
    "🇹🇭 Tailandés": "th",
    "🇻🇳 Vietnamita": "vi"

}

# ======================================================
# VOCES IA
# ======================================================

voces = {

    "🔥 Hombre Viral Español":
    "es-ES-AlvaroNeural",

    "🔥 Mujer Viral Español":
    "es-ES-ElviraNeural",

    "🔥 Hombre TikTok Inglés":
    "en-US-GuyNeural",

    "🔥 Mujer TikTok Inglés":
    "en-US-JennyNeural",

    "🔥 Hombre Francés":
    "fr-FR-HenriNeural",

    "🔥 Mujer Francesa":
    "fr-FR-DeniseNeural",

    "🔥 Hombre Alemán":
    "de-DE-ConradNeural",

    "🔥 Mujer Alemana":
    "de-DE-KatjaNeural",

    "🔥 Hombre Portugués":
    "pt-BR-AntonioNeural",

    "🔥 Mujer Portuguesa":
    "pt-BR-FranciscaNeural",

    "🔥 Hombre Japonés":
    "ja-JP-KeitaNeural",

    "🔥 Mujer Japonesa":
    "ja-JP-NanamiNeural",

    "🔥 Hombre Coreano":
    "ko-KR-InJoonNeural",

    "🔥 Mujer Coreana":
    "ko-KR-SunHiNeural"

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

st.subheader("⚙️ Opciones PRO")

mantener_original = st.checkbox(
    "🎧 Mantener voz original de fondo",
    value=True
)

volumen_original = st.slider(
    "🔉 Volumen voz original",
    0.0,
    1.0,
    0.20
)

velocidad_voz = st.slider(
    "⚡ Velocidad voz IA",
    -50,
    50,
    -15
)

modelo_whisper = st.selectbox(
    "🧠 Calidad IA",
    [
        "tiny",
        "base",
        "small"
    ],
    index=1
)

# ======================================================
# FUNCIÓN GENERAR AUDIO IA
# ======================================================

async def generar_audio(texto, voz, salida, velocidad):

    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate=f"{velocidad}%",
        pitch="+0Hz"
    )

    await communicate.save(salida)

# ======================================================
# PROCESAMIENTO
# ======================================================

if uploaded_file is not None:

    st.video(uploaded_file)

    size_mb = uploaded_file.size / (1024 * 1024)

    st.info(f"📦 Tamaño del video: {size_mb:.2f} MB")

    if st.button("🚀 GENERAR DOBLAJE PRO MAX"):

        try:

            with st.spinner("🔥 Procesando video IA..."):

                # ==================================================
                # CREAR CARPETA TEMPORAL
                # ==================================================

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

                st.info("🎧 Extrayendo audio del video...")

                video = VideoFileClip(video_path)

                audio_path = os.path.join(
                    temp_dir,
                    "audio.wav"
                )

                video.audio.write_audiofile(
                    audio_path,
                    logger=None
                )

                # ==================================================
                # TRANSCRIBIR AUDIO
                # ==================================================

                st.info("🧠 Transcribiendo IA...")

                model = whisper.load_model(
                    modelo_whisper
                )

                result = model.transcribe(
                    audio_path
                )

                texto_original = result["text"]

                st.success("✅ Texto detectado")

                with st.expander("📝 Ver texto original"):

                    st.write(texto_original)

                # ==================================================
                # TRADUCIR TEXTO
                # ==================================================

                st.info("🌍 Traduciendo texto...")

                texto_traducido = GoogleTranslator(
                    source="auto",
                    target=target_lang
                ).translate(texto_original)

                st.success("✅ Traducción completada")

                with st.expander("🌍 Ver traducción"):

                    st.write(texto_traducido)

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
                # NORMALIZAR AUDIO
                # ==================================================

                sonido = AudioSegment.from_file(
                    voz_generada
                )

                sonido = normalize(sonido)

                sonido.export(
                    voz_generada,
                    format="mp3"
                )

                st.success("✅ Voz IA creada")

                # ==================================================
                # CREAR AUDIO FINAL
                # ==================================================

                st.info("🎬 Creando doblaje final...")

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

                # ==================================================
                # CREAR VIDEO FINAL
                # ==================================================

                final_video = video.set_audio(
                    final_audio
                )

                output_path = os.path.join(
                    temp_dir,
                    "doblaje_final.mp4"
                )

                st.info("📦 Exportando video final...")

                final_video.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    preset="ultrafast",
                    threads=2,
                    logger=None
                )

                # ==================================================
                # RESULTADO
                # ==================================================

                st.success("🎉 DOBLAJE COMPLETADO")

                st.video(output_path)

                with open(output_path, "rb") as file:

                    st.download_button(
                        "⬇️ DESCARGAR VIDEO DOBLADO",
                        file,
                        file_name="ANDROIDETV_DOBLAJE_PRO_MAX.mp4",
                        mime="video/mp4"
                    )

        except Exception as e:

            st.error(f"❌ ERROR: {e}")
