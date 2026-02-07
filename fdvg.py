import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - Ultra AI", layout="wide")
st_autorefresh(interval=3000, key="ai_brain_refresh")

# --- الإدارة والأمن ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "أرحب يا عبود.. أنا خويكم الجديد، سولفوا معي زين وأبشروا باللي يسركم. ✨"}], 
        "active_users": set(),
        "ai_mood": 100, # مستوى الرواق (100 رايق، 0 مضغوط)
        "memory": [] # ذاكرة السوالف لتطوير الردود
    }

data = get_manager()

# --- محرك التوليد الذكي (Generative Logic) ---
def generate_dynamic_response(user, text):
    text = text.lower()
    # كلمات تضغط البوت
    stress_words = ["زق", "تبن", "ورع", "غبي", "اشس", "انطم", "حمار", "تيس"]
    
    # إذا المستخدم غلط، ينقص مستوى الرواق
    if any(w in text for w in stress_words):
        data["ai_mood"] -= 25
        if data["ai_mood"] <= 0:
            return random.choice([
                f"أقول يا {user}، انطم واعرف مع مين تتكلم! ماني شغال عند أبوك أنا!",
                f"خلاص قفلت معي.. {user} لا تخليني أهينك قدام العيال، ماني راد عليك لين تتأدب!",
                f"عبود شف هالعينة.. يغلط ويبي أسولف معه؟ والله ما عاد بتشوف حرف زين مني يا {user}."
            ])
        else:
            return random.choice([
                f"يا {user} خلك محترم، أنا جالس أسولف معك بالطيب.. لا تخليني أغير وجهي عليك.",
                f"ما هقيتها منك يا {user}.. ليه الغلط؟ تراني بديت انضغط منك!",
                "بمشيها لك هالمرة عشان عبود، بس لا تعيدها."
            ])

    # إذا الكلام زين، البوت يسولف ويتعلم
    if data["ai_mood"] < 50:
        data["ai_mood"] += 10 # يروق شوي إذا تعاملت معه زين

    responses = [
        f"والله يا {user} كلامك منطقي، توني كنت أفكر في نفس الموضوع!",
        f"ههههههه يا {user} عليك ذبات، ذكرتني بسالفة صارت لي في سيرفر ثاني.",
        f"تدري يا {user}؟ أحس إنك أطلق واحد يسولف اليوم بالمجلس.",
        "يا عيال، عبود وينه؟ نبي نفتح موضوع فلة بعيداً عن الطقطقة."
    ]
    return random.choice(responses)

# --- نظام تسجيل الدخول (القائمة والباسوورد) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول المجلس المشفر")
    u = st.text_input("اسمك").strip()
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if u == ADMIN_USER and p == ADMIN_PWD:
            st.session_state.logged_in, st.session_state.is_admin, st.session_state.username = True, True, u
            st.rerun()
        elif p == NORMAL_PWD and u:
            st.session_state.logged_in, st.session_state.is_admin, st.session_state.username = True, False, u
            data["active_users"].add(u)
            st.rerun()
        else: st.error("البيانات غلط!")
    st.stop()

# --- لوحة التحكم الجانبية ---
with st.sidebar:
    st.title("🛠 التحكم")
    if st.session_state.is_admin:
        if st.button("🧹 مسح الشات"):
            data["messages"] = []
            data["ai_mood"] = 100
            st.rerun()
    st.link_button("🎤 مكالمة المجلس", "https://meet.jit.si/AlRokonYati_Secret")
    st.write(f"المزاج الحالي لركوني: {data['ai_mood']}%")

# --- عرض الشات ---
st.title("🧠 مجلس ركوني المطور")
for i, m in enumerate(data["messages"]):
    is_ai = "🤖" in m["user"]
    with st.chat_message("assistant" if is_ai else "user"):
        st.write(f"**{m['user']}**: {m['content']}")

# --- منطقة الإرسال والتوليد ---
prompt = st.chat_input("سولف مع ركوني..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    # توليد رد فعل ذكي
    with st.spinner("ركوني يكتب..."):
        time.sleep(1) # محاكاة التفكير
        response = generate_dynamic_response(st.session_state.username, prompt)
        data["messages"].append({"user": "🤖 ركوني", "content": response})
    st.rerun()
