import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - Turbo", layout="wide")

PASSWORD = "الركونياتي"

# تهيئة حالة الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# شاشة الدخول
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس المشفر")
    name = st.text_input("وش اسمك؟")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD and name:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
    st.stop()

# مخزن الرسايل المشترك (الذاكرة المركزية)
@st.cache_resource
def get_global_messages():
    return []

all_messages = get_global_messages()

# --- القائمة الجانبية ---
st.sidebar.title(f"هلا {st.session_state.username} 👋")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

# --- منطقة الشات المباشر ---
st.title(" مجلس الركونياتي -  ")

# استخدام "Fragment" لتحديث منطقة الرسايل فقط بسرعة عالية
@st.fragment(run_every="0.5s")
def display_chat():
    # هذا السطر يحدث المنطقة هذي كل نص ثانية
    for msg in all_messages:
        with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
            st.write(f"**{msg['user']}**: {msg['content']}")

display_chat()

# إرسال النص
text = st.chat_input("اكتب هنا..!")
if text:
    all_messages.append({"user": st.session_state.username, "content": text})
    # لا نحتاج rerun هنا لأن الـ fragment سيحدث الصفحة تلقائياً
