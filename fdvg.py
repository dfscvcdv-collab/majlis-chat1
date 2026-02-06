import streamlit as st
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - Pro", layout="wide")

# تحديث تلقائي كل ثانية
st_autorefresh(interval=1000, key="chatupdate")

PASSWORD = "الركونياتي"

@st.cache_resource
def get_manager():
    # إضافة ميزة لمسح الشات إذا علق
    return {"messages": [], "active_users": set()}

data = get_manager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    name = st.text_input("وش اسمك؟").strip()
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD and name and name not in data["active_users"]:
            st.session_state.logged_in = True
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        elif name in data["active_users"]:
            st.error("الاسم مستخدم!")
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"هلا {st.session_state.username} 👋")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

st.sidebar.divider()
st.sidebar.subheader("📁 مشاركة ملفات")
uploaded_file = st.sidebar.file_uploader("اختر ملف", type=None, key="file_up")

if st.sidebar.button("نشر الملف"):
    if uploaded_file:
        # هنا السر: نحفظ الملف كبيانات مستقلة تماماً
        data["messages"].append({
            "user": st.session_state.username,
            "type": "file",
            "file_name": uploaded_file.name,
            "file_data": uploaded_file.getvalue() # حفظ البيانات هنا
        })
        st.sidebar.success("تم الإرسال!")

# زر الطوارئ (إذا علق الشات امسحه من هنا)
if st.sidebar.button("🧹 مسح الشات (للكل)"):
    data["messages"] = []
    st.rerun()

# --- عرض الشات ---
st.title("🎮 مجلس الركونياتي")

for msg in data["messages"]:
    with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
        if msg.get("type") == "file":
            st.write(f"📂 **{msg['user']}** أرسل ملفاً:")
            st.download_button(label=f"📥 تحميل {msg['file_name']}", 
                             data=msg['file_data'], 
                             file_name=msg['file_name'],
                             key=f"dl_{msg['file_name']}_{data['messages'].index(msg)}")
        else:
            # تأكدنا هنا إنه ما يطبع إلا النص عشان ما تطلع الرموز الحمراء
            st.write(f"**{msg['user']}**: {msg.get('content', '')}")

text = st.chat_input("اكتب هنا...")
if text:
    data["messages"].append({"user": st.session_state.username, "type": "text", "content": text})
    st.rerun()
