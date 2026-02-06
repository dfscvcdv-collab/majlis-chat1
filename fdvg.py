import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات واجهة فخمة
st.set_page_config(page_title="مجلس الركونياتي - الإدارة العليا", layout="wide")
st_autorefresh(interval=1000, key="chatupdate")

# --- الحماية والصلاحيات ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(), 
        "muted_users": set(), # المكتومين بالاسم
        "global_mute": False  # كتم الكل فجأة
    }

data = get_manager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🛡️ بوابة دخول مجلس الركونياتي")
    name = st.text_input("ادخل اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    
    if st.button("تسجيل الدخول"):
        if name == ADMIN_USER and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.username = name
            st.rerun()
        elif pwd == NORMAL_PWD and name:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        else:
            st.error("البيانات غلط يا بطل")
    st.stop()

# --- لوحة التحكم الخاصة بعبود (الأدمن) ---
if st.session_state.is_admin:
    st.sidebar.title("🎮 لوحة تحكم عبود")
    
    # كتم الكل فجأة
    st.sidebar.subheader("🔒 إغلاق المجلس")
    if st.sidebar.button("🚨 كتم الشات عن الجميع" if not data["global_mute"] else "🔓 فتح الشات للجميع"):
        data["global_mute"] = not data["global_mute"]
        st.rerun()
    
    # ميوت وفك ميوت لشخص واحد
    st.sidebar.divider()
    st.sidebar.subheader("👤 إدارة المستخدمين")
    target = st.sidebar.selectbox("اختر شخص", sorted(list(data["active_users"])))
    col_mute, col_unmute = st.sidebar.columns(2)
    if col_mute.button("🔇 كتم"):
        data["muted_users"].add(target)
    if col_unmute.button("🔊 فك كتم"):
        data["muted_users"].discard(target)
        
    if st.sidebar.button("🧹 مسح الرسايل"):
        data["messages"] = []
        st.rerun()

st.sidebar.divider()
st.sidebar.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Chat")

# --- منطقة عرض الشات ---
st.title("💬 مجلس الركونياتي")

if data["global_mute"]:
    st.error("🔇 المجلس مغلق حالياً بقرار من عبود (ممنوع الكتابة)")

for i, msg in enumerate(data["messages"]):
    with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
        col_text, col_del = st.columns([0.9, 0.1])
        with col_text:
            if msg["type"] == "image":
                st.write(f"🖼 **{msg['user']}**:")
                st.image(msg["content"], use_container_width=True)
                st.download_button("📥 تحميل", msg["content"], file_name=f"img_{i}.png", key=f"dl_{i}")
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")
        
        # حذف رسالة معينة للأدمن
        if st.session_state.is_admin:
            with col_del:
                if st.button("🗑", key=f"del_{i}"):
                    data["messages"].pop(i)
                    st.rerun()

# --- منطقة الإرسال ---
is_user_muted = st.session_state.username in data["muted_users"]

if (not data["global_mute"] and not is_user_muted) or st.session_state.is_admin:
    col_input, col_file = st.columns([0.8, 0.2])
    
    with col_file:
        img = st.file_uploader("🖼", type=['png','jpg','jpeg'], label_visibility="collapsed")
        if img:
            if st.button("نشر الصورة"):
                data["messages"].append({"user": st.session_state.username, "type": "image", "content": img.getvalue()})
                st.rerun()
                
    text = st.chat_input("اكتب رسالتك هنا...")
    if text:
        data["messages"].append({"user": st.session_state.username, "type": "text", "content": text})
        st.rerun()
elif is_user_muted:
    st.warning("🚫 أنت مكتوم حالياً من قبل الإدارة.")
