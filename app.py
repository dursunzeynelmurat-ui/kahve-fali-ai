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

# --- 2. GEMINI FAL FONKSİYONU (PROMPT Güncellendi) ---
def fal_bak(images_list, user_name, age, burc, status):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f'''
    Sen Sultan Abla adında, tatlı dilli ve hisleri kuvvetli bir falcısın. Geleneksel Türk kahvesi falı bakıyorsun.
    
    Kullanıcı Bilgileri: Adı: {user_name}, Yaşı: {age}, Burcu: {burc}, Medeni Durumu: {status}.
    
    **ÖNEMLİ TALİMAT:** Medeni Durum bilgisini Aşk yorumlarını kişiselleştirmek için kullan, ancak **Burç bilgisini ana fal yorumuna çok fazla katma**. Burç bilgisini sadece en sonda istenen Günlük Burç Yorumu kısmında kullan.
    
    Sana tam 4 adet fotoğraf gönderdim ve bunların sırası ve anlamları şöyledir:
    
    **Fotoğraf 1 (İlk Yüklenen): Fincan Ağzı (Yakın Gelecek):** Fincanın üst kısımları, kişinin o anki ruh hali ve yakın zamanda gerçekleşecek olayları simgeler.
    **Fotoğraf 2 (İkinci Yüklenen): Fincan Yan Açısı (Mevcut Engeller):** Fincanın yan duvarları ve dikey çizgiler, kişinin mevcut hayat yolundaki engelleri veya hızlı çözümleri gösterir.
    **Fotoğraf 3 (Üçüncü Yüklenen): Fincan Ortası/Dibi (Uzun Vadeli Olaylar):** Fincanın altı, kişinin geçmişten gelen etkilerini ve uzun vadede gerçekleşecek önemli olayları temsil eder.
    **Fotoğraf 4 (Dördüncü Yüklenen): Kahve Tabağı (Dış Dünya/Aile/Şans):** Tabak, kişinin aile hayatını, sosyal çevresini ve genel şansını simgeler.
    
    Lütfen tüm bu dört görseli birbirleriyle ilişkilendirerek, kapsamlı ve derinlemesine bir yorum yap.
    
    **İstenen Format:**
    1.  **### 📜 İşte Sultan Abladan Sana Özel Fal Yorumu:** Başlığı altında, sadece telve ve kişisel duruma dayalı (burçsuz) yorumu yap.
    2.  Yorumlarını şu ana başlıklarda topla: Genel Durum, Aşk ve İlişkiler, Kariyer ve Para, Genel Tavsiye.
    3.  Çok mistik, samimi ("Canım", "Kuzum") bir dil kullan.
    4.  Fal yorumunu güzel bir mani veya dilek ile bitir.
    5.  **---** (Ayırıcı Çizgi Koy)
    6.  **### ☀️ Günlük Burç Yorumun:** Başlığı altında, kullanıcının Burcu ({burc}) için kısa, pozitif ve genel bir günlük burç yorumu ekle.
    '''
    
    response = model.generate_content([prompt] + images_list)
    return response.text

# --- 3. ANA UYGULAMA AKIŞI ve ARAYÜZ ---

st.title("☕ Sultan Abla ")
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
st.subheader("4 Fotoğraf Yükle (3 Fincan + 1 Tabak) 📸") 
st.error("**ÇOK ÖNEMLİ SIRA:** Lütfen fotoğrafları **TEK SEFERDE** ve bu sırayla seçin: **1. Fincan Ağzı, 2. Fincan Yan Açısı, 3. Fincan Dibi, 4. Tabak.** Aksi halde fal yanlış çıkar.")

uploaded_files = st.file_uploader(
    "Fotoğrafları Buraya Sürükle veya Tıkla:", 
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if st.button("Falıma Bak 🔮"):
    
    if uploaded_files is None or len(uploaded_files) != 4:
        st.error("Lütfen tam olarak 4 fotoğraf (3 fincan, 1 tabak) yüklediğinizden emin olun.")
    else:
        with st.spinner('Sultan Abla hem fincana bakıyor, hem de burcunu yorumluyor...'):
            try:
                images_to_send = [Image.open(f) for f in uploaded_files]
                
                st.write("Yüklenen Fincanlar (Sıra Kontrolü):")
                cols_img = st.columns(4)
                labels = ["1. Ağız", "2. Yan", "3. Dip", "4. Tabak"]
                for i, img in enumerate(images_to_send):
                    with cols_img[i]:
                        st.image(img, caption=labels[i], width=120)

                fal_yorum = fal_bak(images_to_send, name, age, burc, status) 
                
                st.balloons()
                st.success("Falın Çıktı!")
                # Fal yorumu artık doğrudan modelden gelen formatla yazdırılıyor
                st.markdown(fal_yorum) 
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
