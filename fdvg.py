import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Edition", layout="wide")
st_autorefresh(interval=1500, key="chatupdate")

# --- الحماية والصلاحيات ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(), 
        "muted_users": set(),
        "global_mute": False 
    }

data = get_manager()

# --- وظيفة ذكاء اصطناعي "ركوني" (المطقطق) ---
def rakooni_ai(user_msg):
    responses = [
        "والله يا {user} إنك من جنبها، رح نم بس!",
        "ياخي لا تسولف واجد، صدعت برؤوسنا 🤣",
        "تدري إنك أطلق واحد بالمجلس؟ (أمزح لا تصدق)",
        "هههههههههههههههههه الله يرجك يا شيخ!",
        "أقول.. من عطاك الجوال؟",
        "عبود، تكفى اطرد {user} هذا، سوالفه تجيب النوم 😴"
    ]
    return random.choice(responses).format(user=user_msg)

# --- وظيفة "ذكية" (المثقفة) ---
def thakia_ai():
    questions = [
        "يا ركوني، وش رأيك في الذكاء البشري؟ أشوفه يتدهور 😂",
        "تتوقع عبود بيعطينا ترقية اليوم؟",
        "سؤال للمجلس: وش أكثر شي يضحككم في الحياة؟",
        "يا ركوني لا تطقطق على العيال، خلك محترم شوي!"
    ]
    return random.choice(questions)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول (نفس الكود السابق) ---
if not st.session_state.logged_in:
    st.title("🛡️ بوابة المجلس - AI")
    name = st.text_input("اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
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
    st.stop()

# --- لوحة التحكم (عبود) ---
if st.session_state.is_admin:
    st.sidebar.title("🛠 تحكم الأدمن")
    if st.sidebar.button("🤖 خليهم يسولفون مع بعض"):
        q = thakia_ai()
        data["messages"].append({"user": "🤖 ذكية", "type": "text", "content": q})
        # رد ركوني بعد ثانية
        ans = rakooni_ai("ذكية")
        data["messages"].append({"user": "🤖 ركوني", "type": "text", "content": ans})
        st.rerun()
    
    if st.sidebar.button("🧹 مسح الشات"):
        data["messages"] = []
        st.rerun()

# --- عرض الشات ---
st.title("💬 مجلس الركونياتي المطور")

for i, msg in enumerate(data["messages"]):
    with st.chat_message("assistant" if "🤖" in msg["user"] else "user"):
        st.write(f"**{msg['user']}**: {msg['content']}")

# --- منطقة الإرسال ورد البوت التلقائي ---
prompt = st.chat_input("سولف أو نادِ 'ركوني'...")
if prompt:
    # إضافة رسالة المستخدم
    data["messages"].append({"user": st.session_state.username, "type": "text", "content": prompt})
    
    # رد ركوني إذا أحد ناداه أو عشوائياً (20% نسبة الرد)
    if "ركوني" in prompt.lower() or random.random() < 0.2:
        reply = rakooni_ai(st.session_state.username)
        data["messages"].append({"user": "🤖 ركوني", "type": "text", "content": reply})
    
    # رد ذكية إذا أحد ناداها
    if "ذكية" in prompt.lower():
        data["messages"].append({"user": "🤖 ذكية", "type": "text", "content": "هلا والله، سم؟ أنا هنا عشان أرتب المجلس من طقطقة ركوني."})
    
    st.rerun()
