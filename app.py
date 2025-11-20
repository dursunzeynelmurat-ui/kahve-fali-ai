import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sayfa Ayarları ve Tema
st.set_page_config(
    page_title="Sultan Abla Fal", 
    page_icon="☕",
    layout="centered"
)

# --- 1. API KEY AYARI (Secrets'tan Okuma) ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"] 
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    st.error("Uygulama Hatası: Gemini API Anahtarı (GEMINI_API_KEY) bulunamadı. Lütfen Streamlit Secrets ayarınızı kontrol edin.")
    st.stop()
# -----------------------------

# --- 2. GEMINI FAL FONKSİYONU (3 Resim Destekli) ---
def fal_bak(images_list, user_name, age, burc, status):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    Sen Sultan Abla adında, tatlı dilli ve hisleri kuvvetli bir falcısın. Geleneksel Türk kahvesi falı bakıyorsun.
    
    Kullanıcı Bilgileri: Adı: {user_name}, Yaşı: {age}, Burcu: {burc}, Medeni Durumu: {status}.
    Bu bilgileri kullanarak falı yorumla.
    
    Sana {len(images_list)} adet kahve fincanı veya tabağı fotoğrafı gönderdim. Lütfen her bir fotoğrafı dikkatlice incele.
    
    **Fotoğraf 1:** Genellikle fincanın ağız kısmına yakın olan, yakın gelecek ve kişinin o anki ruh hali hakkında bilgi verir.
    **Fotoğraf 2:** Genellikle fincanın alt kısmına yakın olan, geçmiş veya daha uzun vadeli olayları simgeler.
    **Fotoğraf 3:** Genellikle kahve tabağının fotoğrafı, kişinin dış dünyasını, aile hayatını veya genel şansını temsil eder.
    
    Lütfen tüm bu görselleri birbirleriyle ilişkilendirerek kapsamlı ve derinlemesine bir yorum yap.
    
    Kurallar:
    1. Her bir fotoğraftaki belirgin şekilleri (Kuş, Yılan, Kalp, Yol vb.) benzetim yaparak yorumla.
    2. Yorumlarını şu başlıklarda topla: Genel Durum, Aşk ve İlişkiler, Kariyer ve Para, Genel Tavsiye.
    3. Çok mistik, samimi ("Canım", "Kuzum") bir dil kullan.
    4. Falı güzel bir mani veya dilek ile bitir.
    '''
    
    # Prompt ve resim listesi Gemini'ye gönderiliyor
    response = model.generate_content([prompt] + images_list)
    return response.text

# --- 3. ANA UYGULAMA AKIŞI ve ARAYÜZ ---

st.title("☕ Sultan Abla - Çok Fotoğraflı Fal")
st.markdown("### Kişisel Detaylarını Gir, 3 Fincan Fotoğrafını Yükle! 👇")


# KİŞİSEL GİRİŞLER (Sol Menü)
st.sidebar.header("Kişisel Detaylar 👤")
name = st.sidebar.text_input("Adın nedir?", "Misafir")

col1, col2 = st.sidebar.columns(2)
with col1:
    age = st.number_input("Yaşın kaç?", min_value=18, max_value=99, value=30, step=1)

BURCLAR = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
with col2:
    burc = st.selectbox("Burcun nedir?", options=BURCLAR, index=4)

status = st.radio(
    "Medeni Durumun:",
    ('Evli', 'Bekar', 'İlişkisi Var', 'İlişkisi Yok'),
    horizontal=True
)

st.markdown("---")

# FOTOĞRAF YÜKLEYİCİLER (Ana Ekran)
st.subheader("Fincan Fotoğrafları Yükle (3 Adet)")

uploaded_file1 = st.file_uploader("1. Fincan Ağzı (Yakın Gelecek)", type=["jpg", "png", "jpeg"])
uploaded_file2 = st.file_uploader("2. Fincan Tabanı (Geçmiş/Uzun Vadeli)", type=["jpg", "png", "jpeg"])
uploaded_file3 = st.file_uploader("3. Kahve Tabağı (Dış Dünya/Şans)", type=["jpg", "png", "jpeg"])

all_uploaded_files = [uploaded_file1, uploaded_file2, uploaded_file3]

if st.button("Falıma Bak 🔮"):
    
    # Tüm dosyaların yüklendiğinden emin ol
    if not all(all_uploaded_files):
        st.error("Lütfen 3 fotoğrafı da yükleyin.")
    else:
        with st.spinner('Sultan Abla fincanına odaklanıyor, telveleri okuyor...'):
            try:
                # Yüklenen dosyaları PIL Image nesnelerine dönüştürüyoruz
                images_to_send = [Image.open(f) for f in all_uploaded_files]
                
                # Tüm görselleri yan yana göster
                st.write("Yüklenen Fincanlar:")
                cols_img = st.columns(3)
                for i, img in enumerate(images_to_send):
                    with cols_img[i]:
                        st.image(img, caption=f"Fotoğraf {i+1}", width=150)

                fal_yorum = fal_bak(images_to_send, name, age, burc, status) 
                
                st.balloons()
                st.success("Falın Çıktı!")
                st.markdown("### 📜 İşte Sultan Abladan Sana Özel Yorum:")
                st.write(fal_yorum)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
