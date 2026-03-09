import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import sqlite3
import uuid
import io
import base64

# --- إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('dark_net_v3.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS servers (id TEXT PRIMARY KEY, name TEXT, creator TEXT, invite_code TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS server_members (server_id TEXT, username TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, server_id TEXT, sender TEXT, content TEXT, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

def get_db(): return sqlite3.connect('dark_net_v3.db')

# --- واجهة المستخدم (التصميم المرعب) ---
st.set_page_config(page_title="DARK NET | FINAL ARCHIVE", layout="wide")
st_autorefresh(interval=3000, key="global_sync")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New'; }
    .stButton>button { width: 100%; background-color: #1a0000; color: #ff0000; border: 1px solid #ff0000; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000 !important; color: black !important; }
    .stTextInput>div>div>input { background-color: #000; color: #00ff00 !important; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #000; border-right: 2px solid #ff0000; }
    .member-tag { padding: 5px; border: 1px solid #00ff00; color: #00ff00; border-radius: 5px; margin: 2px; display: inline-block; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- نظام الدخول والتسجيل (مع منع التكرار) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔴 DARK NET TERMINAL</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["ENTRY (دخول)", "NEW IDENTITY (إنشاء حساب)"])
    
    with t1:
        u = st.text_input("ID")
        p = st.text_input("KEY", type="password")
        if st.button("CONNECT"):
            conn = get_db()
            user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
            if user:
                st.session_state.logged_in, st.session_state.username = True, u
                st.rerun()
            else: st.error("❌ خطأ في الهوية أو كلمة المرور")
            
    with t2:
        nu = st.text_input("CHOOSE NEW ID")
        np = st.text_input("CHOOSE NEW KEY", type="password")
        if st.button("GENERATE IDENTITY"):
            if nu and np:
                conn = get_db()
                existing = conn.execute("SELECT username FROM users WHERE username=?", (nu,)).fetchone()
                if existing:
                    st.error("⚠️ هذا الاسم مستخدم بالفعل في المنظمة! اختر اسماً آخر.")
                else:
                    conn.execute("INSERT INTO users VALUES (?, ?)", (nu, np))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.username = True, nu
                    st.success("✅ تم إنشاء الهوية.. جاري الدخول للمنظومة")
                    st.rerun()
            else: st.warning("الرجاء إدخال بيانات كاملة")
    st.stop()

# --- القائمة الجانبية (الأوامر) ---
with st.sidebar:
    st.title(f"👤 {st.session_state.username}")
    if st.button("🔴 خروج آمن"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.divider()
    
    # إنشاء قناة
    with st.expander("📁 تأسيس مجموعة"):
        g_name = st.text_input("اسم المجموعة")
        members = st.text_input("يوزرات الأعضاء (فاصلة بينهم)")
        if st.button("تأسيس"):
            sid = str(uuid.uuid4())[:8]
            inv_code = str(uuid.uuid4())[:5].upper()
            conn = get_db()
            conn.execute("INSERT INTO servers VALUES (?, ?, ?, ?)", (sid, g_name, st.session_state.username, inv_code))
            conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, st.session_state.username))
            for m in members.split(','):
                target = m.strip()
                if target: conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, target))
            conn.commit()
            st.success(f"تم! الكود: {inv_code}")
            st.rerun()

    # انضمام
    with st.expander("🔑 انضمام بكود"):
        code = st.text_input("الكود")
        if st.button("انضمام"):
            conn = get_db()
            serv = conn.execute("SELECT id FROM servers WHERE invite_code=?", (code,)).fetchone()
            if serv:
                conn.execute("INSERT OR IGNORE INTO server_members VALUES (?, ?)", (serv[0], st.session_state.username))
                conn.commit()
                st.rerun()

    st.divider()
    conn = get_db()
    my_servs = conn.execute("SELECT s.id, s.name, s.invite_code FROM servers s JOIN server_members sm ON s.id = sm.server_id WHERE sm.username=?", (st.session_state.username,)).fetchall()
    
    st.markdown("### 🛰️ قنواتك النشطة")
    if st.button("📢 الساحة العامة"):
        st.session_state.active_sid, st.session_state.active_name = "PUBLIC", "الساحة العامة"
    
    for s in my_servs:
        if st.button(f"👁️ {s[1]}"):
            st.session_state.active_sid, st.session_state.active_name = s[0], s[1]

# --- منطقة المحادثة والأعضاء ---
if "active_sid" not in st.session_state:
    st.session_state.active_sid, st.session_state.active_name = "PUBLIC", "الساحة العامة"

st.title(f"📡 {st.session_state.active_name}")

# عرض أعضاء القناة
if st.session_state.active_sid != "PUBLIC":
    conn = get_db()
    current_members = conn.execute("SELECT username FROM server_members WHERE server_id=?", (st.session_state.active_sid,)).fetchall()
    st.markdown("**أعضاء القناة:** " + " ".join([f"<span class='member-tag'>● {m[0]}</span>" for m in current_members]), unsafe_allow_html=True)
    st.divider()

# عرض الرسائل
conn = get_db()
msgs = conn.execute("SELECT sender, content, type FROM messages WHERE server_id=? ORDER BY timestamp ASC", (st.session_state.active_sid,)).fetchall()
for m in msgs:
    with st.chat_message("user"):
        st.write(f"**[{m[0]}]**")
        if m[2] == "text": st.code(m[1], language=None)
        else: st.image(m[1])

# الإرسال
p = st.chat_input("تشفير...")
img = st.sidebar.file_uploader("📤 رفع وثيقة", type=['png','jpg'])

if p:
    conn = get_db()
    conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, p, "text"))
    conn.commit()
    st.rerun()

if img:
    if st.sidebar.button("إرسال الصورة"):
        buf = io.BytesIO()
        Image.open(img).save(buf, format="PNG")
        istr = base64.b64encode(buf.getvalue()).decode()
        conn = get_db()
        conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, istr, "image"))
        conn.commit()
        st.rerun()
