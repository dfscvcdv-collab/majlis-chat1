import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - التحكم الكامل", layout="wide")
st_autorefresh(interval=1000, key="chatupdate")

# --- إعدادات الحماية والأدمن ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(), 
        "muted_users": set()
    }

data = get_manager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول المجلس المشفر")
    name = st.text_input("اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    
    if st.button("دخول"):
        # تشييك إذا كان عبود
        if name == ADMIN_USER and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.username = name
            st.rerun()
        # تشييك إذا كان مستخدم عادي
        elif pwd == NORMAL_PWD and name:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        else:
            st.error("البيانات غلط! تأكد من الاسم وكلمة السر")
    st.stop()

# --- لوحة تحكم الأدمن (عبود) ---
if st.session_state.is_admin:
    st.sidebar.title("🛠 لوحة تحكم عبود")
    
    st.sidebar.subheader("🔇 كتم مستخدم")
    to_mute = st.sidebar.selectbox("اختر الشخص لسكته", list(data["active_users"]))
    if st.sidebar.button(f"أعط {to_mute} ميوت"):
        data["muted_users"].add(to_mute)
        st.sidebar.warning(f"تم كتم {to_mute}")

    if st.sidebar.button("🔓 فك الكتم عن الكل"):
        data["muted_users"] = set()
        st.sidebar.success("الكل يقدر يتكلم الحين")

    if st.sidebar.button("🧹 مسح الشات"):
        data["messages"] = []
        st.rerun()

st.sidebar.divider()
st.sidebar.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Chat")

# --- عرض الشات ---
st.title("🎮 مجلس الركونياتي")

for i, msg in enumerate(data["messages"]):
    # عرض الرسائل بشكل مرتب
    with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
        col1, col2 = st.columns([0.9, 0.1])
        
        with col1:
            if msg["type"] == "image":
                st.write(f"🖼 **{msg['user']}** أرسل صورة:")
                # إظهار الصورة كاملة
                st.image(msg["content"], use_container_width=True)
                # زر التحميل فوق الصورة
                st.download_button("📥 تحميل هذه الصورة", msg["content"], file_name=f"img_{i}.png", key=f"dl_{i}")
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")
        
        # زر الحذف للأدمن عبود
        with col2:
            if st.session_state.is_admin:
                if st.button("❌", key=f"del_{i}"):
                    data["messages"].pop(i)
                    st.rerun()

# --- منطقة الإرسال ---
if st.session_state.username in data["muted_users"]:
    st.error("🚫 أنت مكتوم من قبل عبود. ما تقدر ترسل شي.")
else:
    # خيار إرسال صورة
    with st.expander("🖼 أرسل صورة كاملة"):
        img = st.file_uploader("اختر صورة", type=['png', 'jpg', 'jpeg'], key="img_up")
        if img and st.button("نشر الصورة"):
            data["messages"].append({"user": st.session_state.username, "type": "image", "content": img.getvalue()})
            st.rerun()

    # خيار إرسال نص
    text = st.chat_input("اكتب هنا...")
    if text:
        data["messages"].append({"user": st.session_state.username, "type": "text", "content": text})
        st.rerun()
