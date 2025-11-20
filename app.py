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

# --- 2. GEMINI FAL FONKSİYONU (4 Resim Destekli PROMPT Güncellendi) ---
def fal_bak(images_list, user_name, age, burc, status):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    Sen Sultan Abla adında, tatlı dilli ve hisleri kuvvetli bir falcısın. Geleneksel Türk kahvesi falı bakıyorsun.
    
    Kullanıcı Bilgileri: Adı: {user_name}, Yaşı: {age}, Burcu: {burc}, Medeni Durumu: {status}.
    Bu bilgileri kullanarak falı yorumla.
    
    Sana {len(images_list)} adet, dört farklı açıdan çekilmiş kahve falı fotoğrafı gönderdim. Lütfen her bir fotoğrafı dikkatlice incele.
    
    **Fotoğraf 1: Fincan Ağzı (Yakın Gelecek):** Fincanın üst kısımları, kişinin o anki ruh hali ve yakın zamanda gerçekleşecek olayları simgeler.
    **Fotoğraf 2: Fincan Yan Açısı (Mevcut Engeller):** Fincanın yan duvarları ve dikey çizgiler, kişinin mevcut hayat yolundaki engelleri veya hızlı çözümleri gösterir.
    **Fotoğraf 3: Fincan Ortası/Dibi (Uzun Vadeli Olaylar):** Fincanın altı, kişinin geçmişten gelen etkilerini ve uzun vadede gerçekleşecek önemli olayları temsil eder.
    **Fotoğraf 4: Kahve Tabağı (Dış Dünya/Aile/Şans):** Tabak, kişinin aile hayatını, sosyal çevresini ve genel şansını simgeler.
    
    Lütfen tüm bu dört görseli birbirleriyle ilişkilendirerek, kapsamlı ve derinlemesine bir yorum yap.
    
    Kurallar:
    1. Her bir fotoğraftaki belirgin şekilleri (Kuş, Yılan, Kalp, Yol vb.) benzetim yaparak yorumla.
    2. Yorumlarını şu başlıklarda topla: Genel Durum, Aşk ve İlişkiler, Kariyer ve Para, Genel Tavsiye.
    3. Çok mistik, samimi ("Canım", "Kuzum") bir dil kullan.
    4. Falı güzel bir mani veya dilek ile bitir.
    '''
    
    # Prompt ve resim listesi Gemini'ye gönderiliyor
    response = model.generate_content([prompt] + images_list)
    return response.text

# --- 3. ANA UYGULAMA AKIŞI ve ARAYÜZ (4 YÜKLEYİCİ) ---

st.title("☕ Sultan Abla - Çok Açılı Fal")
st.markdown("### Kişisel Detaylarını Gir, 4 Farklı Fotoğrafı Yükle! 👇")


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
st.subheader("Fincan Fotoğrafları Yükle (4 Adet) 📸")

# YENİ 4 YÜKLEYİCİ TANIMLANIYOR
uploaded_file1 = st.file_uploader("1. Fincan Ağzı (Yakın Gelecek)", type=["jpg", "png", "jpeg"])
uploaded_file2 = st.file_uploader("2. Fincan Yan Açısı (Mevcut Engeller)", type=["jpg", "png", "jpeg"])
uploaded_file3 = st.file_uploader("3. Fincan Ortası/Dibi (Uzun Vadeli Olaylar)", type=["jpg", "png", "jpeg"])
uploaded_file4 = st.file_uploader("4. Kahve Tabağı (Dış Dünya/Aile)", type=["jpg", "png", "jpeg"])

all_uploaded_files = [uploaded_file1, uploaded_file2, uploaded_file3, uploaded_file4] # 4 Dosya listesi
# --- SON ---

if st.button("Falıma Bak 🔮"):
    
    # Tüm 4 dosyanın yüklendiğinden emin ol
    if not all(all_uploaded_files):
        st.error("Lütfen 4 fotoğrafın tamamını yükleyin.")
    else:
        with st.spinner('Sultan Abla fincanın tüm açılarına odaklanıyor...'):
            try:
                # Yüklenen dosyaları PIL Image nesnelerine dönüştürüyoruz
                images_to_send = [Image.open(f) for f in all_uploaded_files]
                
                # Tüm 4 görseli yan yana göster
                st.write("Yüklenen Fincanlar:")
                cols_img = st.columns(4)
                for i, img in enumerate(images_to_send):
                    with cols_img[i]:
                        st.image(img, caption=f"Fotoğraf {i+1}", width=120)

                fal_yorum = fal_bak(images_to_send, name, age, burc, status) 
                
                st.balloons()
                st.success("Falın Çıktı!")
                st.markdown("### 📜 İşte Sultan Abladan Sana Özel Yorum:")
                st.write(fal_yorum)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
