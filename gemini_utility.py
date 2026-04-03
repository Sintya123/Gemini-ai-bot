import os
import json
import streamlit as st
import google.generativeai as genai

# --- KONTROL API KEY (Cloud vs Local) ---
# Cek apakah kita sedang berjalan di Streamlit Cloud (menggunakan Secrets)
if "GOOGLE_GEMINI_API_KEY" in st.secrets:
    GOOGLE_GEMINI_API_KEY = st.secrets["GOOGLE_GEMINI_API_KEY"]
else:
    # Jika tidak ada di secrets, berarti kita di laptop (Local)
    try:
        working_directory = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(working_directory, "config.json")
        with open(config_file_path) as f:
            config_data = json.load(f)
        GOOGLE_GEMINI_API_KEY = config_data["GOOGLE_GEMINI_API_KEY"]
    except FileNotFoundError:
        st.error("API Key tidak ditemukan! Pastikan config.json ada di lokal atau Secrets sudah diisi di Cloud.")
        GOOGLE_GEMINI_API_KEY = None

# Konfigurasi Google AI dengan API Key yang ditemukan
if GOOGLE_GEMINI_API_KEY:
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# --- FUNGSI-FUNGSI UTAMA ---

def load_gemini_pro_model():
    # Menggunakan model terbaru (sesuaikan jika gemini-2.5 sudah stabil)
    return genai.GenerativeModel("gemini-1.5-flash")

def gemini_pro_vision_response(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    if not prompt:
        prompt = "Tolong jelaskan gambar ini secara detail."
    
    response = model.generate_content([prompt, image])
    return response.text

def get_text_embedding(text):
    # Gunakan prefix 'models/' agar tidak error 404
    model_name = "models/text-embedding-004" 
    try:
        embedding_response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="retrieval_query"
        )
        return embedding_response['embedding']
    except Exception as e:
        return None

def get_gemini_response(user_prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_prompt)
    return response.text