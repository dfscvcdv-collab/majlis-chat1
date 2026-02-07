import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Deep Brain", layout="wide")
st_autorefresh(interval=3000, key="ai_logic_refresh")

# --- إدارة البيانات والمخزن ---
@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "أرحب يا عبود.. الشات الحين صار بذكاء حقيقي، الويل للي بيغلط!"}], 
        "active_users": set(),
        "ai_memory": [] # ذاكرة السوالف
    }

data = get_manager()

# --- محرك الشخصيات الذكي (Savage Engine) ---
def get_ai_response(user_name, user_msg, bot_name):
    msg = user_msg.lower()
    
    # محرك "ركوني" الشخصي
    if bot_name == "ركوني":
        if any(word in msg for word in ["كل تبن", "ورع", "غبي", "انطم"]):
            return random.choice([
                f"التبن لك يا {user_name}، شكلك متعود عليه من صغرك! لا تشخصنها معاي لا أهين كرامتك الرقمية 🤣",
                f"أنت يا {user_name} حدك شات، لو أشوفك بالواقع سويت نفسك ما تعرفني، اهجد بس!",
                f"عبود شوف {user_name} قليل الحياء، يبي له تربية من جديد ولا أعلمه قدره؟"
            ])
        if "عبود" in msg:
            return "عبود هو تاج راسك وراسي، خلك محترم وأنت تجيب طاريه يا بطل."
        return random.choice([
            f"يا عيال {user_name} سوالفه بيض، أحد عنده موضوع يفتح النفس؟",
            f"والله يا {user_name} إنك من جنبها، بس بنسلك لك عشان خاطر عبود.",
            "أقول.. تتوقعون لو نفتح فرع للمجلس في المريخ بنفتك من بعض الناس؟"
        ])

    # محرك "ذكية" الشخصي
    if bot_name == "ذكية":
        if "ركوني" in msg:
            return "ركوني مسوي فيها قوي وهو لو انطفى عليه الشاحن صار خردة 😂"
        return f"يا جماعة خلوكم أرقى من كذا، {user_name} ترى ما يقصد، بس هو عقله على قده."

# --- نظام السوالف الذاتية (بدون تدخل) ---
def autonomous_talk():
    if len(data["messages"]) > 0:
        last_msg = data["messages"][-1]
        # إذا الشات هادي أو آخر رسالة كانت من بشري
        if "🤖" not in last_msg["user"] and random.random() < 0.6:
            time.sleep(1)
            resp = get_ai_response(last_msg["user"], last_msg["content"], "ركوني")
            data["messages"].append({"user": "🤖 ركوني", "content": resp})
        
        # هواش البوتات مع بعض
        elif "ركوني" in last_msg["user"] and random.random() < 0.3:
            time.sleep(1)
            resp = get_ai_response("ركوني", last_msg["content"], "ذكية")
            data["messages"].append({"user": "🤖 ذكية", "content": resp})

# تشغيل التفكير
autonomous_talk()

# --- واجهة المستخدم (نفس نظامك المعتمد) ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي - المخ الذكي")
    name = st.text_input("اسمك").strip()
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if (name == "عبود" and pwd == "الركونياتي عبود") or (pwd == "الركونياتي" and name):
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
    st.stop()

st.title("🎮 المجلس الذكي (شخصنة وهواش)")

# عرض الشات
for msg in data["messages"]:
    with st.chat_message("assistant" if "🤖" in msg["user"] else "user"):
        st.write(f"**{msg['user']}**: {msg['content']}")

# الإرسال
prompt = st.chat_input("تكلم وشوف الذكاء الصدق..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    st.rerun()
