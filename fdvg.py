import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. رفع حد المساحة المسموح بها (نظرياً إلى 1 جيجا، لكن يعتمد على قوة السيرفر المجاني)
# ملاحظة: لإتمام هذه الخطوة فعلياً، سنضيف إعداداً في ملف آخر لاحقاً.

st.set_page_config(page_title="مجلس الركونياتي v5", layout="wide")

st_autorefresh(interval=1000, key="chatupdate")

PASSWORD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {"messages": [], "active_users": set()}

data = get_manager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس المشفر")
    name = st.text_input("وش اسمك؟").strip()
    pwd = st.text_input("كلمة السر", type="password")
    
    if st.button("دخول"):
        if pwd == PASSWORD and name and name not in data["active_users"]:
            st.session_state.logged_in = True
            st.session_state.username = name
            data["active_users"].add(name)
            st.rerun()
        elif name in data["active_users"]:
            st.error("الاسم مستخدم حالياً!")
    st.stop()

# --- القائمة الجانبية لإرسال الملفات ---
st.sidebar.title(f"هلا {st.session_state.username} 👋")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

st.sidebar.divider()
st.sidebar.subheader("📁 مشاركة ملفات كبيرة")
uploaded_file = st.sidebar.file_uploader("اختر ملف (فيديو، ZIP، إلخ)", type=None)

if st.sidebar.button("نشر الملف في الشات"):
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        data["messages"].append({
            "user": st.session_state.username,
            "type": "file",
            "file_name": uploaded_file.name,
            "content": file_bytes
        })
        st.sidebar.success(f"تم إرسال {uploaded_file.name}!")

if st.sidebar.button("🚶 خروج"):
    data["active_users"].discard(st.session_state.username)
    st.session_state.logged_in = False
    st.rerun()

# --- عرض الشات ---
st.title(" مجلس الركونياتي - المشفر ")

chat_placeholder = st.container()
with chat_placeholder:
    for msg in data["messages"]:
        with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
            if msg.get("type") == "file":
                st.write(f"📂 **{msg['user']}** أرسل ملفاً:")
                st.download_button(label=f"📥 تحميل: {msg['file_name']}", 
                                 data=msg['content'], 
                                 file_name=msg['file_name'])
            else:
                st.write(f"**{msg['user']}**: {msg['content']}")

text = st.chat_input("اكتب رسالتك...")
if text:
    data["messages"].append({"user": st.session_state.username, "type": "text", "content": text})
    st.rerun()
