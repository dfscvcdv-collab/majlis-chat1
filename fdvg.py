import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي v4", layout="wide")

# التحديث التلقائي السريع (كل ثانية)
st_autorefresh(interval=1000, key="chatupdate")

PASSWORD = "الركونياتي"

# مخزن البيانات المشترك (الرسايل والمستخدمين المتصلين)
@st.cache_resource
def get_manager():
    return {"messages": [], "active_users": set()}

data = get_manager()

# تهيئة حالة الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس المشفر")
    name = st.text_input("وش اسمك؟").strip()
    pwd = st.text_input("كلمة السر", type="password")
    
    if st.button("دخول"):
        if pwd != PASSWORD:
            st.error("كلمة السر غلط يا منيوك")
        elif not name:
            st.warning("لازم تكتب اسمك أول")
        elif name in data["active_users"]:
            st.error(f"الاسم '{name}' موجود حالياً بالشات، اختر اسم ثاني!")
        else:
            st.session_state.logged_in = True
            st.session_state.username = name
            data["active_users"].add(name) # إضافة الاسم لقائمة المتصلين
            st.rerun()
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"هلا {st.session_state.username} 👋")
st.sidebar.link_button(" دخول المكالمه المشفره", "https://meet.jit.si/AlRokonYati_Chat")

# إرسال الصور (تم تعديله ليرسل أكثر من مرة)
st.sidebar.divider()
st.sidebar.subheader("🖼️ إرسال صورة")
img_file = st.sidebar.file_uploader("اختر صورة", type=['png', 'jpg', 'jpeg'], key="img_uploader")
if st.sidebar.button("نشر الصورة"):
    if img_file:
        data["messages"].append({
            "user": st.session_state.username,
            "type": "image",
            "content": img_file.getvalue()
        })
        st.sidebar.success("تم إرسال الصورة!")
        # لا نحتاج لعمل rerun هنا لأن التحديث التلقائي سيتكفل بالأمر

# زر الخروج (عشان يحرر الاسم)
if st.sidebar.button("🚶 تسجيل خروج"):
    data["active_users"].discard(st.session_state.username)
    st.session_state.logged_in = False
    st.rerun()

# --- منطقة الشات المباشر ---
st.title(" مجلس الركونياتي المشفر ")

# عرض الرسائل (نصوص وصور)
chat_placeholder = st.container()
with chat_placeholder:
    for msg in data["messages"]:
        with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
            if msg.get("type") == "image":
                st.write(f"**{msg['user']}** أرسل صورة:")
                st.image(msg["content"], width=300)
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")

# إرسال النص
text = st.chat_input("اكتب هنا..")
if text:
    data["messages"].append({
        "user": st.session_state.username, 
        "type": "text",
        "content": text
    })
    st.rerun()
