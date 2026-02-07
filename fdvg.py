import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Brain", layout="wide")
# التحديث التلقائي ضروري عشان البوتات "يفكرون" كل شوي
st_autorefresh(interval=3000, key="ai_brain_update")

# --- الإعدادات وقاعدة البيانات ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "أرحبوا يا عيال بالمجلس المطور!"}], 
        "active_users": set(),
        "last_ai_time": time.time()
    }

data = get_manager()

# --- مخ البوتات (توليد أفكار حرة) ---
def ai_thinker():
    last_msg = data["messages"][-1] if data["messages"] else None
    current_time = time.time()
    
    # قائمة بالأفكار اللي ممكن يفتحونها من راسهم
    topics = ["الكورة", "السيارات", "الأكل", "الطقطقة على عبود", "الذكاء الاصطناعي", "النوم"]
    
    # 1. إذا كانت آخر رسالة من مستخدم (بشري)، البوتات يردون عليه
    if last_msg and "🤖" not in last_msg["user"]:
        if random.random() < 0.4: # نسبة 40% يردون فوراً
            user_name = last_msg["user"]
            replies = [
                f"🤖 ركوني: يا {user_name}، والله إنك صادق بس لا تعودها 😂",
                f"🤖 ذكية: كلام منطقي يا {user_name}، ركوني تعلم منه شوي!",
                f"🤖 ركوني: {user_name}، بالله اسأل ذكية متى بتعتزل السوالف البيض؟"
            ]
            data["messages"].append({"user": "AI_SYSTEM", "content": random.choice(replies)})
            return

    # 2. إذا الشات هادي (مر 10 ثواني)، واحد يفتح سالفة
    if current_time - data["last_ai_time"] > 10:
        topic = random.choice(topics)
        starts = [
            f"🤖 ركوني: يا عيال شرايكم بـ {topic}؟ أحس إنه سبيكة",
            f"🤖 ذكية: تدرون يا جماعة إن {topic} صار موضة قديمة؟",
            f"🤖 ركوني: عبود، تكفى افتح لنا موضوع عن {topic}، نبي نطقطق شوي"
        ]
        data["messages"].append({"user": "AI_SYSTEM", "content": random.choice(starts)})
        data["last_ai_time"] = current_time
        return

    # 3. إذا البوتات يسولفون مع بعض (رد فعل)
    if last_msg and "🤖 ركوني" in last_msg["user"] and random.random() < 0.3:
        replies = ["🤖 ذكية: ركوني، خلك في حالك وصك فمك", "🤖 ذكية: صادق والله، أول مرة تقول شي مفيد", "🤖 ذكية: ياخي أنت ليش مطقطق على الكل؟"]
        data["messages"].append({"user": "AI_SYSTEM", "content": random.choice(replies)})
    elif last_msg and "🤖 ذكية" in last_msg["user"] and random.random() < 0.3:
        replies = ["🤖 ركوني: بدأت الفلسفة.. يا عيال أحد يسكتها", "🤖 ركوني: ذكية، خفي علينا يا آينشتاين زمانك", "🤖 ركوني: ههههههه طيب طيب بنسلك لك"]
        data["messages"].append({"user": "AI_SYSTEM", "content": random.choice(replies)})

# تشغيل "المخ"
ai_thinker()

# --- شاشة الدخول (نفس الكود السابق) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    name = st.text_input("اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if (name == ADMIN_USER and pwd == ADMIN_PWD) or (pwd == NORMAL_PWD and name):
            st.session_state.logged_in = True
            st.session_state.username = name
            st.session_state.is_admin = (name == ADMIN_USER)
            data["active_users"].add(name)
            st.rerun()
    st.stop()

# --- واجهة الشات ---
st.title("🎮 المجلس الذكي (AI Brain Active)")

for msg in data["messages"]:
    # تنظيف عرض اسم البوت
    display_user = msg["user"].replace("AI_SYSTEM", "")
    content = msg["content"]
    if "🤖" in content: # إذا كان الرد من مخ البوت
        parts = content.split(": ", 1)
        display_user = parts[0]
        content = parts[1]
        
    with st.chat_message("assistant" if "🤖" in display_user else "user"):
        st.write(f"**{display_user}**: {content}")

# إرسال الرسائل
prompt = st.chat_input("اكتب شي وشوف وش يردون عليك...")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    st.rerun()
