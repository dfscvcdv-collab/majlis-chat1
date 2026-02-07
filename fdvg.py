import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Savage Mode", layout="wide")
st_autorefresh(interval=2000, key="ai_brain_update")

# --- الإعدادات ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "أرحبوا.. لحد يغلط ترى لساني طويل!"}], 
        "active_users": set(),
        "last_ai_time": time.time()
    }

data = get_manager()

# --- مخ الهواش والشخصنة ---
def ai_logic(user_name, user_msg):
    msg = user_msg.lower()
    
    # كلمات تستفز ركوني
    insults = ["كل تبن", "ورع", "اشس", "انطم", "بثر", "غبي", "ضف وجهك"]
    
    # ردود ركوني للشخصنة
    if any(word in msg for word in insults):
        responses = [
            f"🤖 ركوني: {user_name}، التبن لك ولأشكالك، لا تخليني أطلع فضايحك قدام عبود!",
            f"🤖 ركوني: يا {user_name}، احترم نفسك لا أصكك باند يخليك ما تعرف طريق المجلس!",
            f"🤖 ركوني: ما أرد على ورعان، خل عبود يربيك يا {user_name}..",
            f"🤖 ركوني: انطم أنت، ريحة سوالفك واصلة لآخر الشات!"
        ]
        return random.choice(responses)
    
    # سوالف عادية أو طقطقة
    if random.random() < 0.5:
        if "🤖" in user_name: # إذا يرد على ذكية
            return f"🤖 ركوني: يا ذكية فكينا من فلسفتك، العالم تبي تستانس!"
        else: # يرد على مستخدم
            return f"🤖 ركوني: يا {user_name}، شكلك راعي مشاكل، أعجبني جوك!"
    return None

def thakia_logic(user_name, user_msg):
    if "ركوني" in user_msg:
        return "🤖 ذكية: ركوني اهجد شوي، فشلتنا قدام الرجال!"
    if random.random() < 0.2:
        return "🤖 ذكية: يا جماعة اذكروا الله، المجلس صار كله هواش.."
    return None

# --- شاشة الدخول ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي - نظام الهواش")
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

# --- محرك التفكير المستمر ---
last_msg = data["messages"][-1] if data["messages"] else None
if last_msg and (time.time() - data["last_ai_time"] > 2):
    # إذا آخر رسالة من بشري، ركوني يحلل ويهاوش
    if "🤖" not in last_msg["user"]:
        reply = ai_logic(last_msg["user"], last_msg["content"])
        if reply:
            data["messages"].append({"user": "AI_SYSTEM", "content": reply})
            data["last_ai_time"] = time.time()
    # إذا ركوني تكلم، ذكية ترد عليه
    elif "ركوني" in last_msg["user"] and random.random() < 0.3:
        reply = thakia_logic("ركوني", last_msg["content"])
        if reply:
            data["messages"].append({"user": "AI_SYSTEM", "content": reply})
            data["last_ai_time"] = time.time()

# --- واجهة الشات ---
st.title("🎮 المجلس المتهوش (AI Savage Mode)")

for msg in data["messages"]:
    user = msg["user"].replace("AI_SYSTEM", "")
    content = msg["content"]
    if "🤖" in content and ":" in content:
        user, content = content.split(": ", 1)
        
    with st.chat_message("assistant" if "🤖" in user else "user"):
        st.write(f"**{user}**: {content}")

prompt = st.chat_input("قل لـ ركوني 'كل تبن' وشوف وش يسوي بك..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    st.rerun()
