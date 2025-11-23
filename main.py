import streamlit as st
from assistant import get_gemini_response, detect_intent
from database import initialize_db, add_event, add_notes, get_events, get_notes
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="Akıllı Asistan",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Veritabanını başlat
initialize_db()

# CSS ile stil ekleme
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .note-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .event-card {
        background-color: #fff5ee;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff6347;
    }
    </style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'page' not in st.session_state:
    st.session_state.page = 'Ana Sayfa'

# Başlık
st.markdown('<div class="main-header">🤖 Akıllı Asistan</div>', unsafe_allow_html=True)

# Sidebar menü
with st.sidebar:
    st.header("📋 Menü")
    
    if st.button("🏠 Ana Sayfa", use_container_width=True):
        st.session_state.page = 'Ana Sayfa'
    
    if st.button("📝 Not Ekle", use_container_width=True):
        st.session_state.page = 'Not Ekle'
    
    if st.button("📅 Etkinlik Ekle", use_container_width=True):
        st.session_state.page = 'Etkinlik Ekle'
    
    if st.button("📖 Notları Göster", use_container_width=True):
        st.session_state.page = 'Notları Göster'
    
    if st.button("🗓️ Etkinlikleri Göster", use_container_width=True):
        st.session_state.page = 'Etkinlikleri Göster'
    
    if st.button("💬 Sohbet Et", use_container_width=True):
        st.session_state.page = 'Sohbet Et'
    
    st.divider()
    st.caption("Akıllı Asistan v1.0")

# Ana içerik alanı
if st.session_state.page == 'Ana Sayfa':
    st.header("Hoş Geldiniz! 👋")
    st.write("Bu akıllı asistan ile notlarınızı ve etkinliklerinizi yönetebilir, yapay zeka ile sohbet edebilirsiniz.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📝 **Not Yönetimi**\n\nNotlarınızı kolayca ekleyin ve görüntüleyin")
    
    with col2:
        st.warning("📅 **Etkinlik Takibi**\n\nÖnemli etkinliklerinizi kaydedin")
    
    with col3:
        st.success("💬 **AI Sohbet**\n\nYapay zeka ile konuşun ve özetler alın")

elif st.session_state.page == 'Not Ekle':
    st.header("📝 Not Ekle")
    
    with st.form("not_form"):
        not_icerigi = st.text_area("Not İçeriği", height=150, placeholder="Notunuzu buraya yazın...")
        submit = st.form_submit_button("💾 Notu Kaydet", use_container_width=True)
        
        if submit:
            if not_icerigi.strip():
                add_notes(not_icerigi.strip())
                st.success("✅ Not başarıyla kaydedildi!")
                st.balloons()
            else:
                st.error("❌ Lütfen not içeriği girin!")

elif st.session_state.page == 'Etkinlik Ekle':
    st.header("📅 Etkinlik Ekle")
    
    with st.form("etkinlik_form"):
        etkinlik = st.text_input("Etkinlik Açıklaması", placeholder="Örn: Doktor randevusu")
        tarih = st.date_input("Etkinlik Tarihi", datetime.now(), format="DD.MM.YYYY")
        submit = st.form_submit_button("💾 Etkinliği Kaydet", use_container_width=True)
        
        if submit:
            if etkinlik.strip():
                add_event(etkinlik.strip(), str(tarih))
                st.success("✅ Etkinlik başarıyla eklendi!")
                st.balloons()
            else:
                st.error("❌ Lütfen etkinlik açıklaması girin!")

elif st.session_state.page == 'Notları Göster':
    st.header("📖 Kaydedilmiş Notlar")
    
    notes = get_notes()
    
    if notes:
        st.info(f"Toplam {len(notes)} not bulundu")
        
        for i, (content, created_at) in enumerate(notes, 1):
            st.markdown(f"""
                <div class="note-card">
                    <strong>Not {i}</strong><br>
                    <small>📅 {created_at}</small><br>
                    <p>{content}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Henüz hiç not eklenmedi. 'Not Ekle' menüsünden not ekleyebilirsiniz.")

elif st.session_state.page == 'Etkinlikleri Göster':
    st.header("🗓️ Etkinlikler")
    
    events = get_events() # [(etkinlik, '2025-11-20'), ...] döner
    
    if events:
        # 1. ADIM: Tarihleri (en yakın tarih en üstte olacak şekilde) sırala
        # x[1] tarihin olduğu sütundur.
        events_sorted = sorted(events, key=lambda x: x[1])
        
        st.info(f"Toplam {len(events)} etkinlik bulundu")
        
        for i, (event, event_date_str) in enumerate(events_sorted, 1):
            # 2. ADIM: Gösterirken Yıl-Ay-Gün formatını Gün.Ay.Yıl'a çevir
            try:
                # String'i tarih objesine çevir
                date_obj = datetime.strptime(event_date_str, "%Y-%m-%d")
                # İstediğimiz formatta string'e çevir
                display_date = date_obj.strftime("%d.%m.%Y")
            except ValueError:
                # Eğer eski kayıtlardan formatı bozuk olan varsa olduğu gibi göster
                display_date = event_date_str

            st.markdown(f"""
                <div class="event-card">
                    <strong>📌 {event}</strong><br>
                    <small>📅 Tarih: {display_date}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Henüz etkinlik girilmemiş. 'Etkinlik Ekle' menüsünden etkinlik ekleyebilirsiniz.")

elif st.session_state.page == 'Sohbet Et':
    st.header("💬 AI ile Sohbet Et")
    
    # Chat geçmişini session state'te tut
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Önceki mesajları göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Kullanıcı inputu
    user_input = st.chat_input("Mesajınızı yazın...")

    if user_input:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Asistan mesajı için placeholder
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("...")  # geçici olarak yazı (soluk görünmeyi engeller)

            with st.spinner("Düşünüyor..."):
                intent = detect_intent(user_input)

                if intent == "not_ozet":
                    notes = get_notes()
                    if not notes:
                        response = "Henüz özetlenecek not bulunmuyor."
                    else:
                        all_notes_text = "\n".join([f"- {note[0]}" for note in notes])
                        prompt = f"Aşağıda bulunan notları özetler misin?\n\n{all_notes_text} \n\n kullanıcı isteği: {user_input}"
                        response = get_gemini_response(prompt)

                elif intent == "etkinlik_ozet":
                    events = get_events()
                    if not events:
                        response = "Özetlenecek etkinlik yok."
                    else:
                        all_events_text = "\n".join([f"- {e[1]}: {e[0]}" for e in events])
                        prompt = f"Aşağıdaki takvim etkinliklerini özetler misin?\n\n{all_events_text}\n\nKullanıcı isteği: {user_input}"
                        response = get_gemini_response(prompt)

                else:
                    response = get_gemini_response(user_input)

            # spinner bittikten sonra placeholder’a yanıtı yazdır
            placeholder.write(response)

            # Mesaj geçmişine ekle
            st.session_state.messages.append({"role": "assistant", "content": response})

    
    # Sohbet geçmişini temizle butonu
   # Sohbet geçmişi varsa temizleme butonunu göster
  # Sohbet geçmişi varsa temizleme butonunu ORTADA göster
    if st.session_state.messages:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Sohbet Geçmişini Temizle", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

