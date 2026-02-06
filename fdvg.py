import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي", layout="wide")

# كلمة السر والبيانات
PASSWORD = "الركونياتي"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    name = st.text_input("وش اسمك؟")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD and name:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
        else:
            st.error("الاسم أو كلمة السر غلط")
    st.stop()

# --- واجهة الشات ---
st.sidebar.title(f"هلا {st.session_state.username}")

# زر المكالمة - بطريقة مبسطة جداً
st.sidebar.write("🎙️ **المكالمة الصوتية**")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

st.title("🎮 شات مجلس الركونياتي")

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(f"**{msg['user']}**: {msg['content']}")
        if "img" in msg:
            st.image(msg["img"], width=250)

# إرسال الصور من الجنب
with st.sidebar:
    st.divider()
    up_img = st.file_uploader("ارسل صورة", type=['png', 'jpg', 'jpeg'], key="uploader")
    if st.button("نشر الصورة"):
        if up_img:
            st.session_state.messages.append({
                "role": "assistant",
                "user": st.session_state.username,
                "content": "أرسل صورة 👇",
                "img": up_img.getvalue()
            })
            st.rerun()

# إرسال النص
text = st.chat_input("اكتب هنا...")
if text:
    st.session_state.messages.append({
        "role": "user", 
        "user": st.session_state.username, 
        "content": text
    })
    st.rerun()
