import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Sultan Abla Fal", page_icon="☕")

st.title("☕ Sultan Abla - Gemini Falcısı")
st.write("Kahve fincanının fotoğrafını yükle, niyetini tut...")

# --- GÜVENLİ ANAHTAR ÇEKME (GitHub'a API Anahtarı sızmaz) ---
try:
    # Anahtarı Streamlit Cloud'daki 'Secrets' (Gizli Kasa) kısmından çek
    api_key = st.secrets["GEMINI_API_KEY"] 
    genai.configure(api_key=api_key)
except:
    st.error("Uygulama Hatası: API Anahtarı bulunamadı. Lütfen Streamlit Cloud 'Secrets' ayarını kontrol edin.")
    st.stop()
# -----------------------------

def fal_bak(image, user_name, age, burc, status):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    Sen Sultan Abla adında, tatlı dilli ve hisleri kuvvetli bir falcısın. Geleneksel Türk kahvesi falı bakıyorsun.
    Kullanıcı Bilgileri: Adı: {user_name}, Yaşı: {age}, Burcu: {burc}, Medeni Durumu: {status}.
    Bu bilgileri kullanarak falı yorumla. Özellikle Burç ve Medeni Durum, Aşk yorumlarını kişiselleştirmek için kullan.
    
    Görevin: Bu kahve fincanı fotoğrafına bakıp yorumlamak.
    
    Kurallar:
    1. Fincanın içindeki şekilleri benzetim yap.
    2. Yorumlarını şu başlıklarda topla: Genel Durum, Aşk ve İlişkiler, Kariyer ve Para.
    3. Çok mistik, samimi ("Canım", "Kuzum") bir dil kullan.
    4. Falı güzel bir mani ile bitir.
    '''
    
    response = model.generate_content([prompt, image])
    return response.text

# --- ARAYÜZ KISMI ---
name = st.text_input("Adın nedir?", "Misafir")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Yaşın kaç?", min_value=18, max_value=99, value=30, step=1)

BURCLAR = ["Koç", "Boğa", "İikizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
with col2:
    burc = st.selectbox("Burcun nedir?", options=BURCLAR, index=4)

status = st.radio(
    "Medeni Durumun:",
    ('Evli', 'Bekar', 'İlişkisi Var', 'İlişkisi Yok'),
    horizontal=True
)

st.markdown("---")
uploaded_file = st.file_uploader("Fincan Fotoğrafı", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("Falıma Bak"):
    with st.spinner('Sultan Abla fincanına odaklanıyor...'):
        try:
            image = Image.open(uploaded_file)
            fal_yorum = fal_bak(image, name, age, burc, status) 
            st.balloons()
            st.success("Falın Çıktı!")
            st.markdown("### 🔮 İşte Sultan Abladan Sana Özel Yorum:")
            st.write(fal_yorum)
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
