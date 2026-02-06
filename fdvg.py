import streamlit as st
import pandas as pd
import requests
from io import StringIO

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي - متصل", layout="wide")

# بيانات الربط بملف جوجل شيت الخاص بك
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1f6YVgCZKeXiFjeVTWrVrBGVv4YW6323DHvH9ldKNig8/export?format=csv"
PASSWORD = "الركونياتي"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- شاشة الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 دخول مجلس الركونياتي")
    name = st.text_input("وش اسمك؟")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if pwd == PASSWORD and name:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.rerun()
    st.stop()

# --- وظيفة جلب الرسائل من جوجل شيت ---
def load_messages():
    try:
        response = requests.get(SHEET_CSV_URL)
        df = pd.read_csv(StringIO(response.text))
        return df.to_dict('records')
    except:
        return []

# --- واجهة الشات ---
st.sidebar.title(f"هلا {st.session_state.username}")
if st.sidebar.button("🔄 تحديث الشات"):
    st.rerun()

st.title("🎮 شات مجلس الركونياتي")

# عرض الرسائل المخزنة في جوجل شيت
messages = load_messages()
for msg in messages:
    if pd.notna(msg.get('content')):
        with st.chat_message("user" if msg['user'] == st.session_state.username else "assistant"):
            st.write(f"**{msg['user']}**: {msg['content']}")

# إرسال نص جديد
# ملاحظة: الإرسال المباشر لجوجل شيت يتطلب إعدادات إضافية (Google Forms أو API)
# كحل سريع ومجاني، استخدم "st.chat_input" للتواصل اللحظي حالياً
text = st.chat_input("اكتب رسالتك هنا...")
if text:
    # هنا يتم عرض الرسالة محلياً، ولجعلها تظهر للكل بشكل دائم
    # يفضل استخدام "Streamlit Google Sheets Connection"
    st.session_state.messages.append({"user": st.session_state.username, "content": text})
    st.rerun()
