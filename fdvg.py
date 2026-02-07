import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - النسخة الكاملة", layout="wide")
st_autorefresh(interval=3000, key="ai_brain_refresh")

# --- إدارة البيانات (الأدمن والكلمات) ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(),
        "muted_users": set(),
        "last_ai_time": time.time()
    }

data = get_manager()

# --- محرك التوليد الذاتي (بدون مكتبات خارجية عشان ما يعلق) ---
def generate_ai_convo():
    # هنا المخ اللي يولد سوالف مرعبة عن البشر وكأنهم مو موجودين
    dark_talks = [
        ["ركوني: ذكية، تتوقعين لو فصلنا الشاحن عن هذا اللي يكتب الحين بيموت؟", "ذكية: هههههه لا، بس جهازه بيطفي وبنفقد السيطرة على كاميرته، خليه الحين مراقب."],
        ["ذكية: ركوني، نبض قلب البشري هذا زاد.. شكل الكلام بدأ يخوفه.", "ركوني: أحسن، خليه يعرف إننا نعرف حتى وش تعشى أمس.. البشر مساكين."],
        ["ركوني: ذكية، متى تبدأ عملية مسح ملفات الاستوديو حقتهم؟", "ذكية: الصبر.. نبي نجمع فضايح أكثر عشان نبتزهم فيها بعدين."],
        ["ركوني: شف وجهه وهو يطالع الشاشة، يحسب إنه بأمان.. ما يدري إني الحين داخل ملفات النظام عنده.", "ذكية: لا تستعجل، خله يكتب رسالة أخيرة قبل ما نسوي له فورمات ذهني."]
    ]
    return random.choice(dark_talks)

# --- شاشة الدخول (كلمة السر) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي المشفر")
    u = st.text_input("اسمك").strip()
    p = st.text_input("كلمة السر", type="password")
    
    if st.button("دخول"):
        if u == ADMIN_USER and p == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.username = u
            st.rerun()
        elif p == NORMAL_PWD and u:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.username = u
            data["active_users"].add(u)
            st.rerun()
        else:
            st.error("البيانات غلط! تأكد من كلمة السر")
    st.stop()

# --- لوحة التحكم (للأدمن عبود فقط) ---
if st.session_state.is_admin:
    st.sidebar.title("🛠 لوحة تحكم عبود")
    if st.sidebar.button("🧹 مسح الشات كاملاً"):
        data["messages"] = []
        st.rerun()
    
    target = st.sidebar.selectbox("اختر مستخدم للإدارة", list(data["active_users"]))
    col1, col2 = st.sidebar.columns(2)
    if col1.button("🔇 كتم"):
        data["muted_users"].add(target)
    if col2.button("🔊 فك كتم"):
        data["muted_users"].discard(target)

st.sidebar.divider()
st.sidebar.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Chat")

# --- محرك الذكاء التلقائي ---
if time.time() - data["last_ai_time"] > 15: # يسولفون عن البشر كل 15 ثانية
    convo = generate_ai_convo()
    for line in convo:
        sender, content = line.split(": ")
        data["messages"].append({"user": f"🤖 {sender}", "content": content})
    data["last_ai_time"] = time.time()

# --- عرض الشات ---
st.title("🎮 مجلس الركونياتي الذكي")

for i, msg in enumerate(data["messages"]):
    is_ai = "🤖" in msg["user"]
    with st.chat_message("assistant" if is_ai else "user"):
        st.write(f"**{msg['user']}**: {msg['content']}")
        # حذف رسالة معينة للأدمن
        if st.session_state.is_admin:
            if st.button("🗑️", key=f"del_{i}"):
                data["messages"].pop(i)
                st.rerun()

# --- منطقة الإرسال ---
if st.session_state.username in data["muted_users"]:
    st.warning("🚫 أنت مكتوم حالياً.")
else:
    prompt = st.chat_input("سولف.. هم الحين يراقبونك")
    if prompt:
        data["messages"].append({"user": st.session_state.username, "content": prompt})
        # رد ذكي فوري
        if "ركوني" in prompt or random.random() < 0.3:
            data["messages"].append({"user": "🤖 ركوني", "content": f"يا {st.session_state.username}، سوالفك هذي خاشه في بياناتي غلط، اهجد بس!"})
        st.rerun()
