import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مجلس الركونياتي v3", layout="wide")

# رابط ملف جوجل شيت (استبدل هذا بالرابط حقك)
# ملاحظة: لتحويل الشيت لقاعدة بيانات حقيقية، نستخدم صيغة الـ CSV للملف
SHEET_ID = "حط_هنا_رابط_الملف_حقك" 

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

# --- واجهة الشات ---
st.sidebar.title(f"هلا {st.session_state.username}")
st.sidebar.link_button("🎤 دخول المكالمة الآن", "https://meet.jit.si/AlRokonYati_Chat")

# زر لتحديث الشات يدوياً
if st.sidebar.button("🔄 تحديث السوالف"):
    st.rerun()

st.title("🎮 شات مجلس الركونياتي")

# محاكي لقاعدة بيانات (لحين ربطك الرسمي بـ Google Sheets API)
# لتجربة سريعة الآن: سنستخدم الـ Cache المشترك
if "shared_msg" not in st.session_state:
    st.session_state.shared_msg = []

# عرض الرسايل
for msg in st.session_state.shared_msg:
    with st.chat_message("user" if msg["user"] == st.session_state.username else "assistant"):
        st.write(f"**{msg['user']}**: {msg['content']}")

# إرسال النص
text = st.chat_input("اكتب هنا والكل بيشوفه...")
if text:
    st.session_state.shared_msg.append({
        "user": st.session_state.username, 
        "content": text
    })
    st.rerun()
