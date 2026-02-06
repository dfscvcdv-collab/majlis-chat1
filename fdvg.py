import streamlit as st
import time

# 1. إعدادات الصفحة والأمان
st.set_page_config(page_title="مجلس الركونياتي", page_icon="🎙️", layout="wide")

# كلمة السر اللي طلبتها
PASSWORD = "الركونياتي"

# تهيئة قاعدة البيانات في الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    with st.form("login_form"):
        name = st.text_input("وش اسمك؟")
        pwd = st.text_input("كلمة السر", type="password")
        submit = st.form_submit_button("دخول")
        
        if submit:
            if pwd == PASSWORD and name:
                st.session_state.logged_in = True
                st.session_state.username = name
                st.success("دخلت يا وحش!")
                st.rerun()
            else:
                st.error("الاسم أو كلمة السر غلط يا صاحبي")
    st.stop()

# --- بعد تسجيل الدخول (واجهة الشات) ---
st.sidebar.title(f"مرحباً، {st.session_state.username} 👋")

# زر المكالمة الصوتية (حل ذكي ومجاني)
st.sidebar.subheader("🎙️ المكالمة الصوتية")
st.sidebar.info("اضغط الزر بالأسفل لفتح غرفة اتصال صوتي مجانية مع العيال")
st.sidebar.markdown(f'<a href="https://meet.jit.si/AlRokonYati_Chat" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#FF4B4B; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🎤 دخول المكالمة الآن</button></a>', unsafe_allow_context=True)

st.title(" شات الركونياتي")
st.write("---")

# عرض الرسائل
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"**{msg['user']}**: {msg['content']}")
            if "image" in msg:
                st.image(msg["image"], width=300)

# منطقة الإرسال (حل مشكلة الصور المتكررة)
with st.sidebar:
    st.subheader("📁 إرسال ملفات")
    img_file = st.file_uploader("ارفع صورة", type=['png', 'jpg', 'jpeg'], key="img_upload")
    if st.button("إرسال الصورة المختارة"):
        if img_file:
            st.session_state.messages.append({
                "role": "assistant",
                "user": st.session_state.username,
                "content": "أرسل صورة 👇",
                "image": img_file.getvalue()
            })
            st.success("تم إرسال الصورة!")
            st.rerun()

prompt = st.chat_input("اكتب رسالتك هنا...")
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "user": st.session_state.username,
        "content": prompt
    })
    st.rerun()

# زر مسح الشات (للمشرفين فقط)
if st.sidebar.button("🧹 مسح الشات للكل"):
    st.session_state.messages = []
    st.rerun()
