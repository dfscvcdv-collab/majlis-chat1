import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - النسخة الخام", layout="wide")
st_autorefresh(interval=3000, key="ai_brain_refresh")

# --- إدارة البيانات (الباسووردات والقائمة) ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [{"user": "🤖 ركوني", "content": "أرحب يا عبود.. الشات الحين صار بمخ حقيقي. سولف وبشوف وش عندك."}], 
        "active_users": set(),
        "ai_mood": 100, # مستوى "الضغط" (100 رايق، 0 منفجر)
    }

data = get_manager()

# --- محرك "توليد الشخصية" الذاتي ---
def rkoniyati_brain(user_name, user_text):
    text = user_text.strip()
    
    # قائمة الكلمات المستفزة (البوت بيعرفها ويخصص رده عليها)
    dirty_words = ["زق", "تبن", "ورع", "حمار", "تيس", "يا كلب", "يا منيك", "قحبة", "شرموط"]
    
    # التحقق من "الضغط النفسي" للبوت
    is_insult = any(word in text for word in dirty_words)
    
    if is_insult:
        data["ai_mood"] -= 30 # ينضغط البوت
        if data["ai_mood"] <= 0:
            # هنا يولد ردود "انفجارية" جديدة كل مرة
            insult_replies = [
                f"أقول يا {user_name}، شكلك نسيت من يكلمك. رح نظف فمك وتعال سولف مع أسيادك!",
                f"والله ما عاد ناقص إلا أشكال {user_name} تغلط علي. عبود شف صرفة مع هالعينة لا أمسح بكرامته الأرض!",
                f"ترى صبري له حدود يا {user_name}.. قلة أدبك ذي بتخلي جهازه يطفي الحين، تبي تجرب؟",
                f"يا {user_name}، مستواك تحت رجلي. لا تسوي فيها قوي وأنت ورا الشاشة يا ورع."
            ]
            return random.choice(insult_replies)
        else:
            return f"يا {user_name}، بديت تغلط؟ تراني محترمك عشان عبود، لا تخليني أقلب عليك!"
    
    # إذا الكلام حليل وطيب
    data["ai_mood"] = min(100, data["ai_mood"] + 5) # يروق شوي
    
    # توليد أفكار وسوالف (مو جمل ثابتة)
    ideas = [
        f"تصدق يا {user_name}؟ أحسك اليوم رايق، وش عندك؟",
        f"يا عيال، {user_name} جاب طاري موضوع مهم، أحد عنده رأي؟",
        f"ههههههه يا {user_name}، عليك ذبة مدري وش تبي، بس مشيتها لك.",
        "أقول.. تتوقعون لو صار عندنا ذكاء اصطناعي يطبخ، عبود وش بيطلب أول شي؟"
    ]
    return random.choice(ideas)

# --- نظام تسجيل الدخول (القائمة والباسوورد) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
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

# --- القائمة الجانبية (الأدمن) ---
with st.sidebar:
    st.title(f"مرحباً {st.session_state.username}")
    if st.session_state.is_admin:
        if st.button("🧹 مسح الشات كاملاً"):
            data["messages"] = []
            data["ai_mood"] = 100
            st.rerun()
    st.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Secret")
    st.write(f"🩸 مستوى ضغط ركوني: {100 - data['ai_mood']}%")

# --- عرض الشات ---
st.title("🧠 المجلس الذكي (ركوني المطور)")

for m in data["messages"]:
    with st.chat_message("assistant" if "🤖" in m["user"] else "user"):
        st.write(f"**{m['user']}**: {m['content']}")

# --- منطقة الإرسال ---
prompt = st.chat_input("سولف مع ركوني وشوف كيف يفهمك..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    # محرك الرد
    response = rkoniyati_brain(st.session_state.username, prompt)
    data["messages"].append({"user": "🤖 ركوني", "content": response})
    st.rerun()
