import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import uuid

# --- إعدادات الهوية البصرية ---
st.set_page_config(page_title="DARK NET | SECRET NETWORK", layout="wide", page_icon="💀")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ff0000; }
    .stApp { background-color: #050505; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New'; text-shadow: 2px 2px #550000; }
    .stButton>button { width: 100%; border-radius: 0px; background-color: #1a0000; color: #ff0000; border: 1px solid #ff0000; }
    .stButton>button:hover { background-color: #ff0000; color: black; box-shadow: 0px 0px 20px #ff0000; }
    .stTextInput>div>div>input { background-color: #0a0a0a; color: #00ff00 !important; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #ff0000; }
    .server-card { padding: 10px; border: 1px solid #444; margin-bottom: 5px; border-radius: 5px; background: #0d0d0d; }
    </style>
    """, unsafe_allow_html=True)

st_autorefresh(interval=3000, key="global_sync")

# --- إدارة قاعدة البيانات (Local Simulation) ---
if "users" not in st.session_state:
    st.session_state.users = {"عبود": "الركونياتي"} # الحساب الافتراضي
if "servers" not in st.session_state:
    st.session_state.servers = {} # {server_id: {"name": "", "members": [], "messages": []}}
if "user_sessions" not in st.session_state:
    st.session_state.logged_in = False

# --- نظام تسجيل الدخول وإنشاء الحساب ---
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
    
    with tab1:
        u = st.text_input("IDENTITY CODE")
        p = st.text_input("PASSKEY", type="password")
        if st.button("AUTHORIZE"):
            if u in st.session_state.users and st.session_state.users[u] == p:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else: st.error("INVALID IDENTITY")
            
    with tab2:
        new_u = st.text_input("NEW IDENTITY")
        new_p = st.text_input("NEW PASSKEY", type="password")
        if st.button("CREATE IDENTITY"):
            if new_u and new_u not in st.session_state.users:
                st.session_state.users[new_u] = new_p
                st.success("Identity Created. Proceed to Login.")
            else: st.error("Identity Taken or Invalid")
    st.stop()

# --- القائمة الجانبية: إدارة السيرفرات ---
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username}")
    if st.button("🔴 LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.divider()
    st.markdown("### 🌐 السيرفرات الخاصة")
    
    # إنشاء سيرفر جديد
    with st.expander("➕ إنشاء سيرفر جديد"):
        s_name = st.text_input("اسم السيرفر")
        target_user = st.text_input("يوزر الشخص المراد إضافته")
        if st.button("تأسيس السيرفر"):
            if target_user in st.session_state.users:
                s_id = str(uuid.uuid4())[:8]
                st.session_state.servers[s_id] = {
                    "name": s_name,
                    "members": [st.session_state.username, target_user],
                    "messages": []
                }
                st.success(f"تم إنشاء سيرفر {s_name}")
            else: st.error("المستخدم غير موجود")

    st.divider()
    # عرض السيرفرات التي ينتمي لها المستخدم فقط
    my_servers = {sid: s for sid, s in st.session_state.servers.items() if st.session_state.username in s["members"]}
    
    selected_server_id = st.radio("اختر قناة الاتصال:", ["الساحة العامة"] + list(my_servers.keys()), 
                                  format_func=lambda x: my_servers[x]["name"] if x in my_servers else x)

# --- منطقة المحادثة ---
if selected_server_id == "الساحة العامة":
    st.title("📢 الساحة العامة (الأرشيف العام)")
    if "public_messages" not in st.session_state: st.session_state.public_messages = []
    messages_list = st.session_state.public_messages
else:
    st.title(f"🔒 سيرفر: {my_servers[selected_server_id]['name']}")
    messages_list = st.session_state.servers[selected_server_id]["messages"]

# عرض الرسائل
for m in messages_list:
    with st.chat_message("user"):
        st.write(f"**{m['user']}**")
        if m["type"] == "text":
            st.code(m["content"], language=None)
        elif m["type"] == "image":
            st.image(m["content"])

# إرسال الرسائل والصور
prompt = st.chat_input("تشفير رسالة...")
col1, col2 = st.sidebar.columns(2)
with col1:
    img_file = st.file_uploader("🖼️ رفع صورة", type=['png','jpg'], label_visibility="collapsed")

if prompt:
    messages_list.append({"user": st.session_state.username, "type": "text", "content": prompt})
    st.rerun()

if img_file:
    if st.sidebar.button("إرسال الصورة المختارة"):
        image = Image.open(img_file)
        messages_list.append({"user": st.session_state.username, "type": "image", "content": image})
        st.rerun()

# --- التذييل ---
st.markdown("<br><br><p style='text-align: center; color: #222;'>ENCRYPTED END-TO-END | NO LOGS SAVED ON MAIN FRAME</p>", unsafe_allow_html=True)
