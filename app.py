import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sayfa Ayarları ve Tema
st.set_page_config(
    page_title="Sultan Abla Fal", 
    page_icon="☕",
    layout="centered"
)

# --- 1. API KEY AYARI ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"] 
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    st.error("Uygulama Hatası: Gemini API Anahtarı (GEMINI_API_KEY) bulunamadı. Lütfen Streamlit Secrets ayarınızı kontrol edin.")
    st.stop()
# -----------------------------

# --- 2. GEMINI FAL FONKSİYONU (Prompt Detaylı Kalacak) ---
def fal_bak(images_list, user_name, age, burc, status):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    Sen Sultan Abla adında, tatlı dilli ve hisleri kuvvetli bir falcısın. Geleneksel Türk kahvesi falı bakıyorsun.
    
    Kullanıcı Bilgileri: Adı: {user_name}, Yaşı: {age}, Burcu: {burc}, Medeni Durumu: {status}.
    Bu bilgileri kullanarak falı yorumla.
    
    Sana tam 4 adet fotoğraf gönderdim ve **bunların sırası ve anlamları şöyledir:**
    
    **Fotoğraf 1 (İlk Yüklenen): Fincan Ağzı (Yakın Gelecek):** Fincanın üst kısımları, kişinin o anki ruh hali ve yakın zamanda gerçekleşecek olayları simgeler.
    **Fotoğraf 2 (İkinci Yüklenen): Fincan Yan Açısı (Mevcut Engeller):** Fincanın yan duvarları ve dikey çizgiler, kişinin mevcut hayat yolundaki engelleri veya hızlı çözümleri gösterir.
    **Fotoğraf 3 (Üçüncü Yüklenen): Fincan Ortası/Dibi (Uzun Vadeli Olaylar):** Fincanın altı, kişinin geçmişten gelen etkilerini ve uzun vadede gerçekleşecek önemli olayları temsil eder.
    **Fotoğraf 4 (Dördüncü Yüklenen): Kahve Tabağı (Dış Dünya/Aile/Şans):** Tabak, kişinin aile hayatını, sosyal çevresini ve genel şansını simgeler.
    
    Lütfen tüm bu dört görseli birbirleriyle ilişkilendirerek, kapsamlı ve derinlemesine bir yorum yap.
    
    Kurallar:
    1. Her bir fotoğraftaki belirgin şekilleri (Kuş, Yılan, Kalp, Yol vb.) benzetim yaparak yorumla.
    2. Yorumlarını şu başlıklarda topla: Genel Durum, Aşk ve İlişkiler, Kariyer ve Para, Genel Tavsiye.
    3. Çok mistik, samimi ("Canım", "Kuzum") bir dil kullan.
    4. Falı güzel bir mani veya dilek ile bitir.
    '''
    
    response = model.generate_content([prompt] + images_list)
    return response.text

# --- 3. ANA UYGULAMA AKIŞI ve ARAYÜZ ---

st.title("☕ Sultan Abla ☕  ")
st.markdown("### 1. Detayları Girin, 2. Fotoğrafları Yükleyin! 👇")


# KİŞİSEL GİRİŞLER (Sol Menü)
st.sidebar.header("Kişisel Detaylar 👤")
name = st.sidebar.text_input("Adın nedir?", "Misafir")

col1, col2 = st.sidebar.columns(2)
with col1:
    age = st.number_input("Yaşın kaç?", min_value=18, max_value=99, value=30, step=1)

BURCLAR = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
with col2:
    burc = st.selectbox("Burcun nedir?", options=BURCLAR, index=4)

status = st.sidebar.radio(
    "Medeni Durumun:",
    ('Evli', 'Bekar', 'İlişkisi Var', 'İlişkisi Yok')
)

st.markdown("---")

# FOTOĞRAF YÜKLEYİCİ (Tek Buton - Ana Ekran)
# Yükleme Etiketi Basitleştirildi
st.subheader("4 Fotoğraf Yükle (3 Fincan + 1 Tabak) 📸") 
st.warning("**ÖNEMLİ SIRA:** Lütfen sırasıyla **Fincan Ağzı, Fincan Yanı, Fincan Dibi ve Tabak** fotoğraflarını seçin.")

uploaded_files = st.file_uploader(
    "Fotoğrafları Buraya Sürükle veya Tıkla:", 
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if st.button("Falıma Bak 🔮"):
    
    # Yüklenen dosya sayısı kontrolü
    if uploaded_files is None or len(uploaded_files) != 4:
        st.error("Lütfen tam olarak 4 fotoğraf (3 fincan, 1 tabak) yüklediğinizden emin olun.")
    else:
        with st.spinner('Sultan Abla fincanın tüm açılarına odaklanıyor...'):
            try:
                # Yüklenen dosyaları PIL Image nesnelerine dönüştürüyoruz
                images_to_send = [Image.open(f) for f in uploaded_files]
                
                # Tüm 4 görseli yan yana göster
                st.write("Yüklenen Fincanlar (Kontrol):")
                cols_img = st.columns(4)
                labels = ["1. Ağız", "2. Yan", "3. Dip", "4. Tabak"]
                for i, img in enumerate(images_to_send):
                    with cols_img[i]:
                        st.image(img, caption=labels[i], width=120)

                fal_yorum = fal_bak(images_to_send, name, age, burc, status) 
                
                st.balloons()
                st.success("Falın Çıktı!")
                st.markdown("### 📜 İşte Sultan Abladan Sana Özel Yorum:")
                st.write(fal_yorum)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
