import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي", layout="wide")

PASSWORD = "الركونياتي"

# تهيئة المخزن المشترك (هذا يخلي الرسايل تظهر للكل)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# شاشة الدخول
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    name = st.text_input("وش اسمك؟")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD and name:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
    st.stop()

# --- القائمة الجانبية (المكالمة والتحديث) ---
st.sidebar.title(f"هلا {st.session_state.username} 👋")

st.sidebar.subheader("🎙️ المكالمة الصوتية")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

st.sidebar.divider()
if st.sidebar.button("🔄 تحديث السوالف"):
    st.rerun()

# --- منطقة الشات ---
st.title("🎮 شات مجلس الركونياتي")

# استخدام st.cache_resource لعمل مخزن رسايل مشترك فعلياً بين كل المستخدمين
@st.cache_resource
def get_global_messages():
    return []

all_messages = get_global_messages()

# عرض الرسايل
for msg in all_messages:
    with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
        st.write(f"**{msg['user']}**: {msg['content']}")

# إرسال نص
text = st.chat_input("اكتب شي والكل بيشوفه...")
if text:
    all_messages.append({"user": st.session_state.username, "content": text})
    st.rerun()
