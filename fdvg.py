import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - نظام الإدارة", layout="wide")
st_autorefresh(interval=1000, key="chatupdate")

# إعدادات الحماية
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
USER_PWD = "الركونياتي"

# مدير البيانات (المخزن المشترك)
@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(), 
        "muted_list": set()  # قائمة الأشخاص المكتومين
    }

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
        elif pwd == USER_PWD and name:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        else:
            st.error("البيانات غلط")
    st.stop()

# --- لوحة تحكم عبود (الأدمن) ---
if st.session_state.is_admin:
    st.sidebar.title("🛠 تحكم الإدارة")
    
    # ميزة الميوت لشخص معين
    st.sidebar.subheader("🚫 كتم شخص محدد")
    target_user = st.sidebar.selectbox("اختر الشخص", list(data["active_users"]))
    if st.sidebar.button(f"كتم {target_user}"):
        data["muted_list"].add(target_user)
        st.sidebar.warning(f"تم كتم {target_user}")
        
    if st.sidebar.button("🔓 فك الكتم عن الجميع"):
        data["muted_list"] = set()
        st.sidebar.success("تم فك الكتم")

    if st.sidebar.button("🧹 مسح الشات كاملاً"):
        data["messages"] = []
        st.rerun()

st.sidebar.divider()
st.sidebar.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Chat")

# --- عرض الشات ---
st.title("🎮 مجلس الركونياتي")

# التحقق إذا كان المستخدم الحالي مكتوم
is_muted = st.session_state.username in data["muted_list"]

for i, msg in enumerate(data["messages"]):
    cols = st.columns([0.9, 0.1])
    with cols[0]:
        with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
            if msg["type"] == "image":
                st.write(f"🖼 **{msg['user']}** أرسل صورة:")
                st.image(msg["content"], use_container_width=True)
                st.download_button("📥 تحميل", msg["content"], file_name=f"img_{i}.png", key=f"dl_{i}")
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")
    
    # زر حذف الرسالة (للأدمن فقط)
    with cols[1]:
        if st.session_state.is_admin:
            if st.button("❌", key=f"del_{i}"):
                data["messages"].pop(i)
                st.rerun()

# --- منطقة الإرسال ---
if is_muted:
    st.error("🚫 أنت مكتوم من قبل الإدارة، ما تقدر ترسل رسايل.")
else:
    # منطقة رفع الصور (بجوار مربع النص)
    with st.expander("🖼 إرسال صورة"):
        img_file = st.file_uploader("اختر صورة", type=['png','jpg','jpeg'])
        if img_file and st.button("نشر الصورة"):
            data["messages"].append({
                "user": st.session_state.username, 
                "type": "image", 
                "content": img_file.getvalue()
            })
            st.rerun()

    prompt = st.chat_input("اكتب رسالتك...")
    if prompt:
        data["messages"].append({
            "user": st.session_state.username, 
            "type": "text", 
            "content": prompt
        })
        st.rerun()
