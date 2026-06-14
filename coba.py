import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import os

# Load API Key dari .env
load_dotenv()

# Konfigurasi LLM
client = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

# Judul aplikasi
st.title("🗺️ GeoMate AI")
st.subheader("Asisten GIS dan QGIS")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(
            content="""
Halo! Saya GeoMate AI.

Saya dapat membantu mengenai:
- GIS
- QGIS
- Remote Sensing
- Sistem Koordinat
- Analisis Spasial

Silakan ajukan pertanyaan.
"""
        )
    ]

# Tampilkan chat sebelumnya
for chat in st.session_state.chat_history:

    if isinstance(chat, HumanMessage):
        role = "user"
    else:
        role = "assistant"

    with st.chat_message(role):
        st.markdown(chat.content)

# Input user
user_input = st.chat_input("Tanyakan sesuatu...")

if user_input:

    # Simpan pesan user
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    # Prompt sistem
    messages = [
        AIMessage(
            content="""
Kamu adalah GeoMate AI.

Kamu adalah chatbot khusus GIS dan QGIS.

Tugasmu:
- Menjawab pertanyaan GIS
- Menjawab pertanyaan QGIS
- Menjelaskan sistem koordinat
- Menjelaskan remote sensing
- Memberikan langkah praktis di QGIS

Gunakan Bahasa Indonesia yang santai dan mudah dipahami.
"""
        )
    ]

    messages.extend(st.session_state.chat_history)

    # Kirim ke model
    response = client.invoke(messages)

    # Simpan jawaban AI
    st.session_state.chat_history.append(response)

    st.rerun()