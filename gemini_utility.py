from email.mime import text
import os
import json
import google.generativeai as genai


#get working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"
config_data = json.load(open(config_file_path))

#loading the api key
GOOGLE_GEMINI_API_KEY = config_data["GOOGLE_GEMINI_API_KEY"]

#configuratiopn google with api key
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-2.5-flash")
    return gemini_pro_model

#enpoint for update pip install -U google-generativeai

#configuration for emmbedng

# List all models that support 'embedContent'
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(f"Model Name: {m.name}")


#function for image captionining
def gemini_pro_vision_response(prompt,image):
    model_name = "gemini-2.5-flash" 
    gemini_model = genai.GenerativeModel(model_name)

    if not prompt:
        prompt = "Tolong jelaskan gambar ini secara detail."
    # Kirim prompt dan image (yang sudah berbentuk PIL Image)
    response = gemini_model.generate_content([prompt, image])
    
    return response.text
  

#function to get embeddings for text
def get_text_embedding(text):
    # Update this to the exact name found in your list_models() output
    model_name = "gemini-embedding-001" 
    
    try:
        embedding_response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="retrieval_query"
        )
        return embedding_response['embedding']
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    #function to get respons from gemini LLM
def get_gemini_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-2.5-flash")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
