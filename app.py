import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sayfa Ayarları
st.set_page_config(
    page_title="Sultan Abla Fal", 
    page_icon="☕",
    layout="centered" # İçeriği ortalıyoruz
)

st.title("☕ Sultan Abla ")
st.markdown("### Kişisel Detaylarını Gir, Falına Bak! 👇")

# --- GÜVENLİ ANAHTAR ÇEKME (Gizli Kasa) ---
try:
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
    ... (Geri kalan prompt metni burada devam ediyor) ...
    '''
    
    response = model.generate_content([prompt, image])
    return response.text

# --- ARAYÜZ KISMI: GİRİŞLERİ SOL MENÜYE TAŞIDIK (st.sidebar) ---

st.sidebar.header("Kişisel Detaylar 👤")

name = st.sidebar.text_input("Adın nedir?", "Misafir")
age = st.sidebar.number_input("Yaşın kaç?", min_value=18, max_value=99, value=30, step=1)

BURCLAR = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
burc = st.sidebar.selectbox("Burcun nedir?", options=BURCLAR, index=4)

status = st.sidebar.radio(
    "Medeni Durumun:",
    ('Evli', 'Bekar', 'İlişkisi Var', 'İlişkisi Yok')
)

st.sidebar.markdown("---")
st.sidebar.info("Tüm bilgileriniz, fal yorumundan hemen sonra silinir.")


# --- ANA EKRAN İÇERİĞİ ---

uploaded_file = st.file_uploader("Fincan Fotoğrafı Yükle:", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("Falıma Bak 🔮"):
    if uploaded_file is not None:
        with st.spinner('Sultan Abla fincanına odaklanıyor, telveleri okuyor...'):
            try:
                image = Image.open(uploaded_file)
                
                # Fincan fotoğrafını önizle
                st.image(image, caption="Yüklenen Fincan", width=300)
                
                fal_yorum = fal_bak(image, name, age, burc, status) 
                
                st.balloons()
                st.success("Falın Çıktı!")
                st.markdown("### 📜 İşte Sultan Abladan Sana Özel Yorum:")
                st.write(fal_yorum)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
