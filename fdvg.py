import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي", page_icon="🎙️", layout="wide")

PASSWORD = "الركونياتي"

# 2. تهيئة البيانات
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
                st.rerun()
            else:
                st.error("الاسم أو كلمة السر غلط يا صاحبي")
    st.stop()

# --- واجهة الشات الرئيسية ---
st.sidebar.title(f"مرحباً، {st.session_state.username} 👋")

# زر المكالمة الصوتية (تم تصحيح السطر المسبب للخطأ)
st.sidebar.subheader("🎙️ المكالمة الصوتية")
st.sidebar.info("اضغط الزر لفتح غرفة اتصال صوتي")
voice_link = "https://meet.jit.si/AlRokonYati_Chat"
st.sidebar.markdown(f'<a href="{voice_link}" target="_blank"><button style="width:100%; background-color:#FF4B4B; color:white; border:none; padding:10px; border-radius:5px;">🎤 دخول المكالمة</button></a>', unsafe_allow_context=True)

st.title(" شات الركونياتي")
st.write("---")

# عرض الرسائل القديمة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"**{msg['user']}**: {msg['content']}")
        if "image" in msg:
            st.image(msg["image"], width=300)

# منطقة إرسال الصور (في القائمة الجانبية)
with st.sidebar:
    st.write("---")
    st.subheader("📁 إرسال صور")
    img_file = st.file_uploader("اختر صورة", type=['png', 'jpg', 'jpeg'], key="img_upload")
    if st.button("إرسال الصورة"):
        if img_file:
            st.session_state.messages.append({
                "role": "assistant",
                "user": st.session_state.username,
                "content": "أرسل صورة 👇",
                "image": img_file.getvalue()
            })
            st.rerun()

# منطقة إرسال النص
prompt = st.chat_input("اكتب رسالتك...")
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "user": st.session_state.username,
        "content": prompt
    })
    st.rerun()

# زر مسح الشات
if st.sidebar.button("🧹 مسح الشات"):
    st.session_state.messages = []
    st.rerun()
