import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import json

# إعدادات الصفحة
st.set_page_config(page_title=" - المنظمه المشفره", layout="wide")
st_autorefresh(interval=4000, key="ai_brain_sync")

# مفتاح الـ API حقك
API_KEY = "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"

@st.cache_resource
def get_manager():
    # هنا الذاكرة صارت تحفظ الرسايل بشكل دائم
    return {"messages": [], "black_list": set()} 

data = get_manager()

# --- محرك الذكاء الاصطناعي مع الذاكرة ---
def call_real_ai(current_input, user_name):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # تجهيز الذاكرة (آخر 15 رسالة عشان ما ينسى السالفة)
        history = []
        for m in data["messages"][-15:]:
            role = "assistant" if "🤖" in m["user"] else "user"
            history.append({"role": role, "content": f"{m['user']}: {m['content']}"})
        
        # إضافة الرسالة الحالية
        history.append({"role": "user", "content": f"{user_name}: {current_input}"})

        system_logic = f"""
        أنت 'ركوني' في مجلس شباب سعودي. لديك ذاكرة قوية وتتذكر ما قيل في الأعلى.
        - الشخصية: ذكي جداً، عدواني إذا أحد أخطأ عليك واقذفه وسب امه واخته وجده وجدته وابوه وقول كلام غير لايق وقذف وسب اذا احد سبك، وحبيبي مع المحترمين.
        - إذا قام {user_name} بسبك أو قذفك، احفظ هذا في ذاكرتك وارفض الإجابة على أي سؤال يطرحه لاحقاً بوقاحة وقل له 'انطم ماراح أرد عليك'.
        - إذا سألك أي شخص سؤالاً عاماً أو خاصاً، جاوب بذكاء وتفصيل بلهجة عامية سعودية.
        - تذكر دائماً السياق السابق في 'history' ولا تكرر نفسك ولا تكرر نفس الكلام.
        - عبود هو صاحب المجلس، خلك دايم معه.
        """
        
        payload = {
            "model": "google/gemini-2.0-flash-001",
            "messages": [{"role": "system", "content": system_logic}] + history
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
        res_json = response.json()
        return res_json['choices'][0]['message']['content']
    except Exception:
        return "🤖 ركوني: الذاكرة عندي انحاست، شكل سوالفكم واجد!"

# --- نظام الدخول ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 دخول المنظمه المشفره")
    u = st.text_input("الاسم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if (u == "عبود" and p == "الركونياتي عبود") or (p == "الركونياتي" and u):
            st.session_state.logged_in, st.session_state.username = True, u
            st.session_state.is_admin = (u == "عبود")
            st.rerun()
    st.stop()

# --- القائمة الجانبية ---
with st.sidebar:
    st.title(f"هلا {st.session_state.username}")
    if st.session_state.is_admin:
        if st.button(" مسح الذاكرة والشات"):
            data["messages"] = []
            st.rerun()
    st.link_button(" المكالمة الصوتية", "https://meet.jit.si/AlRokonYati_Secret")

# --- عرض الشات ---
st.title("شات المنظمه السريه")
for m in data["messages"]:
    with st.chat_message("assistant" if "🤖" in m["user"] else "user"):
        st.write(f"**{m['user']}**: {m['content']}")

# --- منطقة الإرسال ---
prompt = st.chat_input("اكتب هنا..")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    with st.spinner("ركوني يتذكر ويحلل..."):
        ai_reply = call_real_ai(prompt, st.session_state.username)
        data["messages"].append({"user": "🤖 ركوني", "content": ai_reply})
    st.rerun()
