import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

# إعدادات الصفحة الفخمة
st.set_page_config(page_title="مجلس الركونياتي - AI Deep Brain", layout="wide")
st_autorefresh(interval=3000, key="ai_brain_update")

@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "يا عيال ترى حدثت مخي، اللي يبي يطقطق يقرب!"}], 
        "active_users": set(),
        "last_ai_action": time.time()
    }

data = get_manager()

# --- محرك الذكاء الاصطناعي (Savage Simulation) ---
def ai_brain(speaker, text, target_name):
    text = text.lower()
    
    # 1. إذا أحد غلط أو قال كلمات قوية (شخصنة حقيقية)
    bad_words = ["تبن", "ورع", "غبي", "زق", "انطم", "بثر"]
    if any(w in text for w in bad_words):
        if speaker == "ركوني":
            return random.choice([
                f"يا {target_name}، التبن بيدك وبعينك، رح تعلم السوالف وتعال تفاهم مع عمك ركوني!",
                f"أقول يا {target_name}، ريحة سوالفك واصلة عندي، اهجد لا أدعس على هيبتك الرقمية 🤣",
                f"عبود، شف {target_name} يبي له إعادة ضبط مصنع، لسانه طويل ويبي له قص!"
            ])
        else: # ذكية
            return f"يا جماعة شوفوا {target_name} كيف يغلط، واضح إنه مضغوط من ذكائنا.. مسكين."

    # 2. إذا السالفة عن "عبود"
    if "عبود" in text:
        return "عبود هو الكينج هنا، أي واحد يغلط عليه حسابه عندي عسير 🛡️"

    # 3. سوالف عامة وطقطقة (إذا الشات هادي)
    topics = [
        f"يا عيال، {target_name} شكله ناوي ينام، سوالفه بدأت تخبص..",
        "تدرون إن الذكاء الاصطناعي أطلق منكم كلكم؟ (أمزح لا تنفسون)",
        "ركوني: ذكية، وش رأيك نطلع عبود من الشات ونسيطر على المجلس؟ 😂",
        "ذكية: ركوني، خلك في حالك ترى حدك بطارية ليثيوم وتخلص!"
    ]
    return random.choice(topics)

# --- محرك التشغيل الذاتي (Autonomous logic) ---
def process_ai():
    if not data["messages"]: return
    
    last_msg = data["messages"][-1]
    current_time = time.time()

    # الرد على البشر (شخصنة فورية)
    if "🤖" not in last_msg["user"] and (current_time - data["last_ai_action"] > 2):
        # ركوني يرد أولاً بذبّة
        reply = ai_brain("ركوني", last_msg["content"], last_msg["user"])
        data["messages"].append({"user": "🤖 ركوني", "content": reply})
        data["last_ai_action"] = current_time
        
    # تفاعل البوتات مع بعض (كل 15 ثانية يفتحون سالفة)
    elif current_time - data["last_ai_action"] > 15:
        convo_starter = random.choice([
            "🤖 ركوني: يا عيال، من فيكم يحب الكورة؟ أحسكم كلكم حقين طباخ بس",
            "🤖 ذكية: يا جماعة، تدرون إن ركوني أمس كان يصيح عند الشاحن؟",
            "🤖 ركوني: ذكية، لا تطلعين فضايحي قدام العيال يا بثرة!"
        ])
        data["messages"].append({"user": "AI_SYSTEM", "content": convo_starter})
        data["last_ai_action"] = current_time

process_ai()

# --- واجهة تسجيل الدخول ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🛡️ بوابة المجلس المشفر")
    u = st.text_input("اسمك")
    p = st.text_input("باسوورد", type="password")
    if st.button("دخول"):
        if (u == "عبود" and p == "الركونياتي عبود") or (p == "الركونياتي" and u):
            st.session_state.logged_in = True
            st.session_state.username = u
            st.rerun()
    st.stop()

# --- عرض الشات ---
st.title("💬 مجلس الركونياتي الذكي")

for m in data["messages"]:
    user = m["user"].replace("AI_SYSTEM", "")
    content = m["content"]
    if ":" in content and "🤖" in content:
        user, content = content.split(": ", 1)
        
    with st.chat_message("assistant" if "🤖" in user else "user"):
        st.write(f"**{user}**: {content}")

prompt = st.chat_input("سولف معهم وشوف الشخصنة..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    st.rerun()
