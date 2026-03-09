import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
from PIL import Image
import base64

# --- إعدادات الهوية البصرية المرعبة ---
st.set_page_config(page_title="DARK NET | ARCHIVE 666", layout="wide", page_icon="💀")

# حقن CSS لتغيير شكل الموقع بالكامل
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ff0000; }
    .stApp { background-color: #050505; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New', Courier, monospace; text-shadow: 2px 2px #550000; }
    .stButton>button { width: 100%; border-radius: 0px; background-color: #220000; color: white; border: 1px solid #ff0000; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff0000; color: black; box-shadow: 0px 0px 15px #ff0000; }
    .stTextInput>div>div>input { background-color: #111; color: #00ff00 !important; border: 1px solid #333; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff0000; }
    .stChatMessage { background-color: #0d0d0d; border: 1px border-left: 5px solid #ff0000; margin-bottom: 10px; border-radius: 5px; }
    /* ستايل لنسخ النص */
    .copy-box { padding: 10px; background: #1a1a1a; border: 1px dashed #444; color: #bbb; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

st_autorefresh(interval=5000, key="dark_sync")

# --- إدارة البيانات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- نظام الدخول ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔴 SYSTEM BREACH REQUIRED</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("IDENTITY")
        p = st.text_input("ACCESS CODE", type="password")
        if st.button("INITIALIZE"):
            if (u == "عبود" and p == "الركونياتي عبود") or (p == "الركونياتي" and u):
                st.session_state.logged_in, st.session_state.username = True, u
                st.session_state.is_admin = (u == "عبود")
                st.rerun()
            else: st.error("ACCESS DENIED: INVALID CREDENTIALS")
    st.stop()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("### 💀 الوحدة المركزية")
    st.write(f"المستخدم الحالي: **{st.session_state.username}**")
    st.divider()
    
    # ميزة رفع الصور
    uploaded_file = st.file_uploader("📤 رفع وثيقة سرية (صورة)", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        if st.button("إرسال الصورة للمنظمة"):
            image = Image.open(uploaded_file)
            st.session_state.messages.append({"user": st.session_state.username, "type": "image", "content": image})
            st.success("تم تشفير ورفع الصورة")
    
    st.divider()
    if st.session_state.is_admin:
        if st.button("🧨 تدمير السجلات (Clear)"):
            st.session_state.messages = []
            st.rerun()
    
    st.link_button("📡 قناة الاتصال المشفرة", "https://meet.jit.si/AlRokonYati_Secret")

# --- عرض الأرشيف (الشات) ---
st.markdown(f"## 🕸️ أرشيف المنظمة: {st.session_state.username}")

for idx, m in enumerate(st.session_state.messages):
    with st.chat_message("user"):
        st.write(f"**[{m['user']}]**")
        
        if m["type"] == "text":
            # عرض النص مع خاصية النسخ عبر st.code
            st.code(m["content"], language=None) 
            st.caption("اضغط على المربع أعلاه لنسخ النص")
        
        elif m["type"] == "image":
            st.image(m["content"], use_container_width=True)
            st.caption("⚠️ وثيقة بصرية مصنفة")

# --- منطقة الإدخال ---
prompt = st.chat_input("أدخل البيانات هنا...")
if prompt:
    st.session_state.messages.append({"user": st.session_state.username, "type": "text", "content": prompt})
    st.rerun()

# --- تذييل الصفحة ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444;'>PROPERTY OF THE ORGANIZATION - UNIFIED ARCHIVE v6.6.6</p>", unsafe_allow_html=True)
