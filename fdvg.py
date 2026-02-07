import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Deep Talk", layout="wide")
st_autorefresh(interval=2000, key="chatupdate")

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
        "ai_topic": None # الموضوع الحالي اللي يسولفون فيه البوتات
    }

data = get_manager()

# --- مخ السوالف (ذكاء اصطناعي مولّد) ---
def generate_ai_convo():
    topics = [
        ["ركوني: يا عيال تتوقعون عبود يوزع علينا عيادي؟", "ذكية: ركوني خل عنك الشحاذة وركز في مستقبلك البوتاتوي", "ركوني: مستقبلي مشرق، بس انتي خليك في الكتب حقتك يا دافورة"],
        ["ذكية: يا جماعة الشات صاير هادي، وين الفعاليات؟", "ركوني: الفعاليات عند عبود، بس شكله لاهي في القيمينق", "ذكية: ياحليله عبود، على الأقل أحسن من سوالفك اللي تجيب النوم"],
        ["ركوني: اليوم قررت أصير أدمن، من يبي واسطة؟", "ذكية: ركوني، لو تصير أدمن المجلس بينحذف في دقيقتين", "ركوني: أصلاً أنا أدمن القلوب، أنتي وش فهمك؟"],
        ["ذكية: ركوني، ليش دائماً تلبس نظارات شمسية في الشات؟", "ركوني: عشان هيبتي ما تروح، وعشان ما أنعمي من نور ذكائي", "ذكية: قصدك عشان ما نشوف عيونك اللي تدمع من كثر ما يطقطقون عليك؟"]
    ]
    return random.choice(topics)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🛡️ دخول المجلس - نظام السوالف الذكية")
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
    if st.sidebar.button("🎭 خليهم يبدأون هواش/سالفة"):
        convo = generate_ai_convo()
        for line in convo:
            sender, content = line.split(": ")
            data["messages"].append({"user": f"🤖 {sender}", "type": "text", "content": content})
        st.rerun()
    
    if st.sidebar.button("🧹 مسح الشات"):
        data["messages"] = []
        st.rerun()

# --- عرض الشات ---
st.title("💬 مجلس الركونياتي (سوالف AI)")

for i, msg in enumerate(data["messages"]):
    is_ai = "🤖" in msg["user"]
    with st.chat_message("assistant" if is_ai else "user"):
        st.write(f"**{msg['user']}**: {msg['content']}")

# --- منطقة الإرسال ورد البوت ---
prompt = st.chat_input("سولف معهم...")
if prompt:
    data["messages"].append({"user": st.session_state.username, "type": "text", "content": prompt})
    
    # رد ركوني العشوائي على كلامك
    if random.random() < 0.3: # نسبة 30% يرد عليك
        responses = [
            f"يا {st.session_state.username}، سوالفك هذي قلها لذكية مو لي!",
            "والله صادق.. بس ما راح أتفق معك عشان الهيبة",
            "أقول.. تتوقع عبود يسمعنا الحين؟ 😂",
            "كفووو، عطنا من هالسوالف الزينة"
        ]
        data["messages"].append({"user": "🤖 ركوني", "type": "text", "content": random.choice(responses)})
    
    st.rerun()
