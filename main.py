import streamlit as st
import os
from streamlit_option_menu import option_menu

from gemini_utility import gemini_pro_vision_response, load_gemini_pro_model, get_text_embedding, get_gemini_response
from PIL import Image 

#install piloow for generate image pip install Pillow

working_directory = os.path.dirname(os.path.abspath(__file__))

#setting up page conviguration
st.set_page_config(
    page_title="Chatbot Gemini",
    page_icon="🤖📖",
    layout="centered",
    initial_sidebar_state="auto"
)

with st.sidebar:
    selected = option_menu(
        "Gemini AI",
        ["Chatbot", "Image Generator", "Embed text","Ask Anything"],
        menu_icon="brain", icons=["chat-dots", "image", "file-earmark-text", "question-circle"],
        default_index=0,

    )


#function to translete role 
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role 
    
if selected == "Chatbot":
    gemini_pro_model = load_gemini_pro_model()

#initialize chat session in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = gemini_pro_model.start_chat(history=[])

#display the chat history
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

#input field for user to enter message
# user_prompt = st.chat_input("Type your message here...")
# if user_prompt:
#     st.chat_message("user").markdown(user_prompt)

#     gemini_response = st.session_state.chat_session.send_message(user_prompt)

#     #disply gemini-pro response
#     with st.chat_message("assistant"):
#         st.markdown(gemini_response.text)


 # Konten halaman
if selected == "Chatbot":
    st.title("🤖 Gemini Chatbot")
    st.write("Halaman chatbot")

elif selected == "Image Generator":
    st.title("🖼 Image Generator")
    st.write("Halaman generator gambar")

elif selected == "Embed text":
    st.title("📄 Text Embedding")
    st.write("Halaman embedding text")

elif selected == "Ask Anything":
    st.title("❓Ask Anything")
    st.write("Tanya apa saja ke AI")

#ask anything page
if selected == "Chatbot":
    user_question = st.text_input("Ask anything to Gemini:")
    
    if st.button("Get Answer"):
        with st.spinner("Getting answer..."):
            answer = get_gemini_response(user_question)
            st.success("Answer received!")
            st.write(f"**Answer:** {answer}")
#image captioning page
if selected == "Image Generator":
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        # Tampilkan gambar di UI
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Ambil input prompt dari user
        user_prompt = st.text_input("Enter a prompt for the image captioning:")

        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                # PERBAIKAN: Konversi file upload menjadi objek Image PIL
                img = Image.open(uploaded_image)
                
                # Kirim objek 'img' (PIL), bukan 'uploaded_image' (Streamlit object)
                caption = gemini_pro_vision_response(user_prompt, img)
                
                st.success("Caption generated!")
                st.write(f"**Caption:** {caption}")

#text embedding page
if selected == "Embed text":
    user_text = st.text_area("Enter text to get embedding:")
    
    if st.button("Get Embedding"):
        with st.spinner("Generating embedding..."):
            embedding = get_text_embedding(user_text)
            st.success("Embedding generated!")
            st.write(f"**Embedding:** {embedding}")

#ask anything page
if selected == "Ask Anything":
    user_question = st.text_input("Ask anything to Gemini:")
    
    if st.button("Get Answer"):
        with st.spinner("Getting answer..."):
            answer = get_gemini_response(user_question)
            st.success("Answer received!")
            st.write(f"**Answer:** {answer}")