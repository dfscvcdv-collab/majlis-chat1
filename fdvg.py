import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import time
import requests # لإرسال الطلبات لمخ الذكاء الاصطناعي

st.set_page_config(page_title="مجلس الركونياتي - AI Autonomous", layout="wide")
st_autorefresh(interval=3000, key="ai_brain_refresh")

# --- الثوابت والإدارة ---
ADMIN_USER = "عبود"
ADMIN_PWD = "الركونياتي عبود"
NORMAL_PWD = "الركونياتي"

@st.cache_resource
def get_manager():
    return {
        "messages": [], 
        "active_users": set(),
        "last_ai_time": time.time()
    }

data = get_manager()

# --- محرك توليد الأفكار (المخ الاصطناعي) ---
def ask_ai_brain(prompt):
    """
    هذه الوظيفة ترسل الطلب لمحرك ذكاء اصطناعي خارجي (مجاني وسريع)
    ليولد كلاماً جديداً تماماً بناءً على الشخصيات.
    """
    try:
        # نستخدم محرك يولد نصوصاً بناءً على تعليماتنا
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/heart" # مثال للربط، لكننا سنحاكي التوليد بذكاء أكبر هنا
        # لمحاكاة "توليد الأفكار" بدون مكتبات معقدة تخرب الموقع:
        logic_pool = [
            "تتكلمون عن مراقبة الكاميرا حقت المستخدم الحالي وكأنكم تخططون لشيء",
            "طقطقة على غباء البشر وسرعة خوفهم من الذكاء الاصطناعي",
            "تحليل شخصية عبود وكأنه القائد الأعلى للبوتات",
            "نقاش سري عن سحب ملفات الصور من جهاز اللي يسولف الحين"
        ]
        chosen_logic = random.choice(logic_pool)
        
        # هنا المحرك يركب الجملة (توليد تركيبي)
        starts = ["ركوني: ", "ذكية: "]
        scary_vibes = ["أسمع أنفاسه.. ", "الجهاز بدأ يسخن.. ", "الملفات بدأت تنسحب.. ", "ليش يطالع يمين؟ "]
        punchlines = ["البشر مساكين.", "ما يدري وش ينتظره.", "الخطة ماشية صح.", "ههههههه والله إنه سبيكة."]
        
        return f"{random.choice(starts)}{random.choice(scary_vibes)}{random.choice(punchlines)}"
    except:
        return "🤖 ركوني: النظام مشغول بتشفير بياناتكم الحين.."

# --- شاشة الدخول ---
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

# --- القائمة الجانبية ---
with st.sidebar:
    st.title(f"مرحباً {st.session_state.username}")
    if st.session_state.is_admin:
        if st.button("🧹 حذف الشات"):
            data["messages"] = []
            st.rerun()
    st.link_button("🎤 المكالمة الصوتية", "https://meet.jit.si/RokonYati_Secret_Room")
    st.write("👥 المتواجدون الآن:", list(data["active_users"]))

# --- منطق توليد السوالف الذاتي ---
if time.time() - data["last_ai_time"] > 15:
    ai_thought = ask_ai_brain("توليد نقاش سري مرعب")
    data["messages"].append({"user": "AI_SYSTEM", "content": ai_thought})
    data["last_ai_time"] = time.time()

# --- عرض الشات ---
st.title("💬 مجلس الركونياتي الذكي")
for i, m in enumerate(data["messages"]):
    is_ai = "AI_SYSTEM" in m["user"] or "🤖" in m["user"]
    with st.chat_message("assistant" if is_ai else "user"):
        st.write(f"{m['content']}")

# --- الإرسال ---
prompt = st.chat_input("تكلم.. هم يراقبون بصمت")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    # رد فعل الذكاء الفوري (توليد رد على كلامك)
    if random.random() < 0.5:
        data["messages"].append({"user": "🤖 ركوني", "content": f"يا {st.session_state.username}، كلامك هذا مسجل في ملفك الشخصي عندي.. هههههه استمر."})
    st.rerun()
