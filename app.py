import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_oauth import OAuth2
import json # OAuth yanıtını işlemek için

# Sayfa Ayarları
st.set_page_config(
    page_title="Sultan Abla Fal", 
    page_icon="☕",
    layout="centered"
)

# --- 1. GİZLİ ANAHTARLARIN VE GEMINI API AYARI ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"] 
    genai.configure(api_key=gemini_api_key)
    
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    REDIRECT_URI = st.secrets.get("OAUTH_REDIRECT_URI", "http://localhost:8501") # Streamlit Cloud'da otomatik belirlenir
    
except Exception as e:
    st.error(f"Uygulama Hatası: Gizli anahtarlar eksik. {e}")
    st.stop()

# --- 2. OAUTH MANTIĞI (GMAIL LOGIN) ---
oauth_config = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
    'token_url': 'https://oauth2.googleapis.com/token',
    'refresh_token_url': None,
    'redirect_uri': REDIRECT_uri,
    'scope': 'openid email profile',
    'client_kwargs': {'scope': 'openid email profile'}
}
oauth = OAuth2(
    client_id=oauth_config['client_id'],
    client_secret=oauth_config['client_secret'],
    authorize_url=oauth_config['authorize_url'],
    token_url=oauth_config['token_url'],
    redirect_uri=oauth_config['redirect_uri'],
    scope=oauth_config['scope']
)

# --- 3. TOKEN VE PROFİL YÖNETİMİ ---
def initialize_user_session(user_info):
    user_email = user_info.get('email')
    if user_email not in st.session_state:
        st.session_state[user_email] = {
            'tokens': 3,
            'logged_in': True,
            'name': user_info.get('name', user_email.split('@')[0]),
            'email': user_email
        }
        st.success(f"Hoş geldiniz, {st.session_state[user_email]['name']}! 3 ücretsiz tokeniniz yüklendi.")
    else:
        st.session_state[user_email]['logged_in'] = True
        st.info(f"Tekrar hoş geldiniz, {st.session_state[user_email]['name']}!")
    
    st.session_state.current_user_email = user_email
    st.rerun()

def logout_user():
    if 'current_user_email' in st.session_state:
        st.session_state[st.session_state.current_user_email]['logged_in'] = False
        del st.session_state.current_user_email
    st.rerun()
    

# --- 4. GEMINI FAL FONKSİYONU (Birden Fazla Resim Alacak Şekilde Güncellendi) ---
# images_list artık bir liste olacak
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
    
    # Prompt'u ve resim listesini aynı anda gönderiyoruz
    response = model.generate_content([prompt] + images_list)
    return response.text

# --- 5. ANA UYGULAMA AKIŞI ---

st.title("☕ Sultan Abla - Gmail Profilli Falcısı")

if 'current_user_email' in st.session_state:
    user_email = st.session_state.current_user_email
    user_data = st.session_state[user_email]

    st.sidebar.header(f"Profil: {user_data['name']}")
    st.sidebar.markdown(f"**💰 Kalan Token:** **{user_data['tokens']}**")

    if st.sidebar.button("🪙 5 Token Yükle (Simülasyon)"):
        st.session_state[user_email]['tokens'] += 5
        st.sidebar.success("5 Token yüklendi! İyi fallar.")
        st.rerun()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Çıkış Yap"):
        logout_user()

    st.subheader("Kişisel Detaylar ve Fal Baktırma")
    st.info("Fal baktırmak 1 Token'dır.")

    col1, col2 = st.columns(2)
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
    st.subheader("Fincan Fotoğrafları Yükle (3 Adet)")

    # --- YENİ: ÜÇ ADET FOTOĞRAF YÜKLEYİCİ ---
    uploaded_file1 = st.file_uploader("1. Fincan Ağzı (Yakın Gelecek)", type=["jpg", "png", "jpeg"])
    uploaded_file2 = st.file_uploader("2. Fincan Tabanı (Geçmiş/Uzun Vadeli)", type=["jpg", "png", "jpeg"])
    uploaded_file3 = st.file_uploader("3. Kahve Tabağı (Dış Dünya/Şans)", type=["jpg", "png", "jpeg"])

    all_uploaded_files = [uploaded_file1, uploaded_file2, uploaded_file3]
    
    if st.button("Falıma Bak (1 Token Harca) 🔮"):
        
        # Tüm dosyaların yüklendiğinden emin ol
        if not all(all_uploaded_files):
            st.error("Lütfen 3 fotoğrafı da yükleyin.")
        elif user_data['tokens'] <= 0:
            st.error("Tokenin kalmadı! Lütfen sol menüden Token yükle.")
        else:
            st.session_state[user_email]['tokens'] -= 1 
            st.sidebar.markdown(f"**💰 Kalan Token:** **{st.session_state[user_email]['tokens']}**")

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

                    fal_yorum = fal_bak(images_to_send, user_data['name'], age, burc, status) 
                    st.balloons()
                    st.success("Falın Çıktı!")
                    st.markdown("### 📜 İşte Sultan Abladan Sana Özel Yorum:")
                    st.write(fal_yorum)
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}. Token geri yüklendi.")
                    st.session_state[user_email]['tokens'] += 1
                    st.rerun()
    
# --- 6. LOGİN EKRANI (GİRİŞ YAPILMADIYSA) ---
else:
    st.subheader("Gmail ile Giriş Yap veya Hesap Oluştur")
    
    token = oauth.authorize_button("Google ile Giriş Yap", icon="https://www.google.com/favicon.ico", state='random')

    if token:
        import jwt 
        try:
             id_token = token.get('id_token')
             if id_token:
                 user_info = jwt.decode(id_token, options={"verify_signature": False})
                 initialize_user_session(user_info)
             else:
                 st.error("Giriş başarısız. ID token alınamadı. Google Developer Console ayarlarınızı kontrol edin.")
        except Exception as e:
             st.error(f"Giriş sırasında hata: {e}. Lütfen Client ID, Client Secret ve Redirect URIs ayarlarınızı kontrol edin.")
             
    st.markdown("---")
    st.info("Giriş yapmadan fal baktıramazsınız. Giriş yaparak 3 ücretsiz token kazanın.")
