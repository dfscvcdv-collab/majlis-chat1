import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="مجلس الركونياتي - لوحة التحكم", layout="wide")
st_autorefresh(interval=1000, key="chatupdate")

# إعدادات الأدمن والمستخدمين
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
USER_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {"messages": [], "active_users": set(), "mute": False}

data = get_manager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول المجلس")
    name = st.text_input("اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    
    if st.button("دخول"):
        if name == ADMIN_USER and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.username = name
            st.rerun()
        elif pwd == USER_PWD and name and name not in data["active_users"]:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        else:
            st.error("البيانات غلط أو الاسم مكرر")
    st.stop()

# --- لوحة التحكم (للأدمن فقط) ---
if st.session_state.is_admin:
    st.sidebar.title("🛠 لوحة تحكم الأدمن")
    if st.sidebar.button("🔇 كتم/إلغاء كتم الشات"):
        data["mute"] = not data["mute"]
        st.sidebar.success("تم تغيير حالة الشات")
    
    if st.sidebar.button("🧹 مسح كل الشات"):
        data["messages"] = []
        st.rerun()

st.sidebar.divider()
st.sidebar.write(f"المستخدم: {st.session_state.username}")
st.sidebar.link_button("🎤 المكالمة", "https://meet.jit.si/AlRokonYati_Chat")

# --- عرض الشات ---
st.title("🎮 مجلس الركونياتي")
if data["mute"]:
    st.warning("⚠️ الشات مكتوم حالياً من قبل الأدمن")

for i, msg in enumerate(data["messages"]):
    cols = st.columns([0.9, 0.1])
    with cols[0]:
        with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
            if msg["type"] == "image":
                st.write(f"🖼 **{msg['user']}**:")
                st.image(msg["content"], use_container_width=True)
                st.download_button("📥 تحميل الصورة", msg["content"], file_name=f"img_{i}.png", key=f"dl_{i}")
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")
    
    # زر الحذف للأدمن فقط
    with cols[1]:
        if st.session_state.is_admin:
            if st.button("❌", key=f"del_{i}"):
                data["messages"].pop(i)
                st.rerun()

# --- إرسال الرسائل ---
if not data["mute"] or st.session_state.is_admin:
    col_msg, col_img = st.columns([0.8, 0.2])
    
    with col_img:
        img_file = st.file_uploader("🖼", type=['png','jpg','jpeg'], label_visibility="collapsed")
        if img_file:
            if st.button("نشر"):
                data["messages"].append({"user": st.session_state.username, "type": "image", "content": img_file.getvalue()})
                st.rerun()
                
    text = st.chat_input("اكتب هنا...")
    if text:
        data["messages"].append({"user": st.session_state.username, "type": "text", "content": text})
        st.rerun()
