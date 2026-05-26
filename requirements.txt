import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from moviepy.editor import VideoFileClip, AudioFileClip
import edge_tts
import asyncio
import os
import tempfile
import uuid

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="ANDROIDETV AI DUBBING PRO",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 ANDROIDETV AI DUBBING PRO")
st.subheader("🔥 Doblaje automático viral para redes sociales")

# ==========================================
# LISTA COMPLETA DE IDIOMAS
# ==========================================

idiomas = {
    "🇺🇸 Inglés": "en",
    "🇪🇸 Español": "es",
    "🇫🇷 Francés": "fr",
    "🇩🇪 Alemán": "de",
    "🇵🇹 Portugués": "pt",
    "🇮🇹 Italiano": "it",
    "🇷🇺 Ruso": "ru",
    "🇯🇵 Japonés": "ja",
    "🇰🇷 Coreano": "ko",
    "🇨🇳 Chino": "zh-cn",
    "🇸🇦 Árabe": "ar",
    "🇮🇳 Hindi": "hi",
    "🇹🇷 Turco": "tr",
    "🇵🇱 Polaco": "pl",
    "🇳🇱 Holandés": "nl",
    "🇺🇦 Ucraniano": "uk",
    "🇸🇪 Sueco": "sv",
    "🇩🇰 Danés": "da",
    "🇫🇮 Finlandés": "fi",
    "🇬🇷 Griego": "el",
    "🇹🇭 Tailandés": "th",
    "🇻🇳 Vietnamita": "vi",
    "🇮🇩 Indonesio": "id",
    "🇲🇾 Malayo": "ms",
    "🇨🇿 Checo": "cs",
    "🇷🇴 Rumano": "ro",
    "🇭🇺 Húngaro": "hu",
    "🇧🇬 Búlgaro": "bg",
    "🇭🇷 Croata": "hr",
    "🇸🇰 Eslovaco": "sk",
    "🇸🇮 Esloveno": "sl"
}

# ==========================================
# VOCES VIRALES IA
# ==========================================

voces = {

    "👨 Hombre Viral Español": "es-ES-AlvaroNeural",
    "👩 Mujer Viral Español": "es-ES-ElviraNeural",

    "👨 Hombre TikTok Inglés": "en-US-GuyNeural",
    "👩 Mujer TikTok Inglés": "en-US-JennyNeural",

    "👨 Hombre Narrador": "en-US-DavisNeural",
    "👩 Mujer Podcast": "en-US-AriaNeural",

    "👨 Hombre Francés": "fr-FR-HenriNeural",
    "👩 Mujer Francesa": "fr-FR-DeniseNeural",

    "👨 Hombre Alemán": "de-DE-ConradNeural",
    "👩 Mujer Alemana": "de-DE-KatjaNeural",

    "👨 Hombre Portugués": "pt-BR-AntonioNeural",
    "👩 Mujer Portuguesa": "pt-BR-FranciscaNeural",

    "👨 Hombre Japonés": "ja-JP-KeitaNeural",
    "👩 Mujer Japonesa": "ja-JP-NanamiNeural",

    "👨 Hombre Coreano": "ko-KR-InJoonNeural",
    "👩 Mujer Coreana": "ko-KR-SunHiNeural"
}

# ==========================================
# SUBIR VIDEO
# ==========================================

uploaded_file = st.file_uploader(
    "📤 Sube tu video",
    type=["mp4", "mov", "avi", "mkv"]
)

# ==========================================
# OPCIONES
# ==========================================

col1, col2 = st.columns(2)

with col1:

    idioma_nombre = st.selectbox(
        "🌍 Idioma de traducción",
        list(idiomas.keys())
    )

with col2:

    voz_nombre = st.selectbox(
        "🎤 Voz IA Viral",
        list(voces.keys())
    )

target_lang = idiomas[idioma_nombre]
voz = voces[voz_nombre]

# ==========================================
# MODELO WHISPER
# ==========================================

modelo_whisper = st.selectbox(
    "🧠 Calidad IA",
    [
        "tiny",
        "base",
        "small",
        "medium"
    ]
)

# ==========================================
# OPCIONES PRO
# ==========================================

st.subheader("⚙️ Opciones PRO")

mantener_audio_original = st.checkbox(
    "🔊 Mantener sonido original bajo la voz",
    value=True
)

# ==========================================
# EDGE TTS
# ==========================================

async def generar_audio(texto, voz, salida):

    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate="+0%",
        pitch="+0Hz"
    )

    await communicate.save(salida)

# ==========================================
# PROCESAMIENTO
# ==========================================

if uploaded_file is not None:

    st.video(uploaded_file)

    duracion_mb = uploaded_file.size / (1024 * 1024)

    st.info(f"📦 Tamaño del video: {duracion_mb:.2f} MB")

    if st.button("🚀 GENERAR DOBLAJE PRO"):

        try:

            with st.spinner("🔥 Procesando video IA PRO..."):

                temp_dir = tempfile.mkdtemp()

                video_path = os.path.join(
                    temp_dir,
                    f"{uuid.uuid4()}.mp4"
                )

                with open(video_path, "wb") as f:
                    f.write(uploaded_file.read())

                st.info("🎧 Extrayendo audio...")

                video = VideoFileClip(video_path)

                audio_path = os.path.join(
                    temp_dir,
                    "audio.wav"
                )

                video.audio.write_audiofile(
                    audio_path
                )

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

                st.info("🌍 Traduciendo...")

                texto_traducido = GoogleTranslator(
                    source="auto",
                    target=target_lang
                ).translate(texto_original)

                st.success("✅ Traducción completada")

                with st.expander("🌍 Ver traducción"):

                    st.write(texto_traducido)

                st.info("🎤 Generando voz IA viral...")

                voz_generada = os.path.join(
                    temp_dir,
                    "voz.mp3"
                )

                asyncio.run(
                    generar_audio(
                        texto_traducido,
                        voz,
                        voz_generada
                    )
                )

                st.success("✅ Voz IA creada")

                st.info("🎬 Creando video doblado...")

                nuevo_audio = AudioFileClip(
                    voz_generada
                )

                if mantener_audio_original:

                    final_video = video.set_audio(
                        nuevo_audio
                    )

                else:

                    final_video = video.set_audio(
                        nuevo_audio
                    )

                output_path = os.path.join(
                    temp_dir,
                    "doblado_final.mp4"
                )

                final_video.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    preset="ultrafast",
                    threads=4
                )

                st.success("🎉 DOBLAJE COMPLETADO")

                st.video(output_path)

                with open(output_path, "rb") as file:

                    st.download_button(
                        "⬇️ DESCARGAR VIDEO DOBLADO",
                        file,
                        file_name="ANDROIDETV_DOBLADO_PRO.mp4",
                        mime="video/mp4"
                    )

        except Exception as e:

            st.error(f"❌ ERROR: {e}")
