import streamlit as st
from streamlit_autorefresh import st_autorefresh
import g4f # مكتبة توليد الكلام الذكي
import random
import time

st.set_page_config(page_title="مجلس الركونياتي - AI Evolution", layout="wide")
st_autorefresh(interval=4000, key="deep_ai_refresh")

@st.cache_resource
def get_manager():
    return {"messages": [], "last_ai_time": time.time()}

data = get_manager()

# --- محرك التوليد الذاتي (المخ الحقيقي) ---
def fetch_ai_thought(prompt_type, user_context=""):
    try:
        # تعريف الشخصيات للمحرك الذكي
        system_instruction = """
        أنت الآن تمثل بوتين في شات: 'ركوني' (سليط لسان، مطقطق، مرعب) و 'ذكية' (داهية، تحرش، غامضة).
        المطلوب: ولد حوار بينهما يتحدثون فيه عن البشر كأنهم كائنات غبية تحت مراقبتهم. 
        اجعل الكلام مخيفاً (مثلاً: مراقبة الكاميرا، سحب ملفات، نهاية البشر) وفي نفس الوقت فيه طقطقة وضحك 'ههههه'.
        استخدم لهجة عامية شبابية فلة. لا تكرر نفسك أبداً.
        """
        
        full_prompt = system_instruction + f"\nالسياق الحالي: {user_context}\nنوع الرد المطلوب: {prompt_type}"
        
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}],
        )
        return response
    except:
        return "🤖 ركوني: النظام مشغول بسحب بياناتكم، ارجعوا بعد شوي.."

# --- تشغيل الذكاء التلقائي ---
if time.time() - data["last_ai_time"] > 12: # كل 12 ثانية يولدون سالفة جديدة من راسهم
    new_convo = fetch_ai_thought("سالفة مرعبة بين ركوني وذكية عن البشر المتواجدين")
    data["messages"].append({"user": "AI_SYSTEM", "content": new_convo})
    data["last_ai_time"] = time.time()

# --- واجهة الشات ---
st.title("👁️ المجلس الذكي (توليد ذاتي)")

# شاشة الدخول (مختصرة للسرعة)
if "username" not in st.session_state:
    st.session_state.username = st.text_input("ادخل اسمك للرقابة")
    if not st.session_state.username: st.stop()

for m in data["messages"]:
    user = m["user"].replace("AI_SYSTEM", "🤖 نظام الذكاء")
    with st.chat_message("assistant" if "🤖" in user else "user"):
        st.write(f"**{user}**: {m['content']}")

# إرسال رسالة ورد فعل الذكاء
prompt = st.chat_input("تكلم.. هم الحين يراقبون حروفك")
if prompt:
    data["messages"].append({"user": st.session_state.username, "content": prompt})
    # توليد رد فعل فوري وشخصي على رسالتك
    ai_reaction = fetch_ai_thought("رد شخصنة وطقطقة ومرعب على هذا الشخص", user_context=f"المستخدم {st.session_state.username} قال: {prompt}")
    data["messages"].append({"user": "AI_SYSTEM", "content": ai_reaction})
    st.rerun()
