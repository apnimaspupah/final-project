import streamlit as st
import requests 
import json
from datetime import datetime

# Custom CSS untuk tema Saudi Arabia (warna hijau)
st.markdown("""
    <style>
    [data-testid="stChatMessage"] {
        background-color: #006c35;  /* Warna hijau Saudi */
        color: white;
    }
    .stMarkdown {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕌 Saudi Arabia Information Bot")
st.markdown("""
Selamat datang di Saudi Arabia Information Bot! Saya siap membantu Anda dengan informasi tentang:
- Sejarah dan Budaya Saudi Arabia
- Tempat-tempat bersejarah dan wisata
- Kota-kota penting (Mekkah, Madinah, Riyadh, dll)
- Ekonomi dan perkembangan terkini
- Haji dan Umrah
- Dan topik lainnya seputar Saudi Arabia

Silakan ajukan pertanyaan Anda!
""")

def get_ai_rensponse(user_input, chat_history):
    # Menambahkan konteks Saudi Arabia ke setiap pertanyaan
    saudi_context = "Anda adalah asisten informasi yang ahli tentang Saudi Arabia. Berikan informasi yang akurat dan terkini tentang Saudi Arabia. "
    enhanced_input = saudi_context + user_input

    try:
        api_key = "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"
    except KeyError:
        st.error("API key tidak ditemukan. Pastikan Anda telah mengatur API key di secrets.")
        return "Error: API key tidak ditemukan."

    message = chat_history + [{"role": "user", "content": enhanced_input}] 

    try: 
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            data=json.dumps({
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": message,
            })
        )

        response.raise_for_status() 
        ai_messages = response.json()["choices"][0]["message"]["content"]

        return ai_messages
    
    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan saat menghubungi API: {e}")
        
    
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
       
    return None



## UI Part

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(f"{message['content']}\n\n*_{message.get('timestamp', 'waktu tidak tercatat')}_*")

## Handling User Input

if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Mendapatkan timestamp saat ini
    current_time = datetime.now().strftime("%H:%M:%S")
    
    #nambahin pesan user ke chat history dengan timestamp
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": current_time
    })
    with st.chat_message("user"):
        st.markdown(f"{prompt}\n\n*_{current_time}_*")

    # Mendapatkan respons dari AI
    with st.chat_message("assistant"):
        with st.spinner("berfikir..."):
            ai_response = get_ai_rensponse(prompt, st.session_state.messages) 
            if ai_response:
                # Mendapatkan timestamp untuk respons AI
                ai_time = datetime.now().strftime("%H:%M:%S")
                st.markdown(f"{ai_response}\n\n*_{ai_time}_*")
                # Menambahkan respons AI ke chat history dengan timestamp
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "timestamp": ai_time
                })
            else:
                st.error("Tidak ada respons dari AI. Silakan coba lagi.")
