import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import sqlite3
import uuid
import io
import base64

# --- إعداد قاعدة البيانات المتقدمة ---
def init_db():
    conn = sqlite3.connect('dark_net_v2.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS servers (id TEXT PRIMARY KEY, name TEXT, creator TEXT, invite_code TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS server_members (server_id TEXT, username TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, server_id TEXT, sender TEXT, content TEXT, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

# --- وظائف النظام ---
def get_db(): return sqlite3.connect('dark_net_v2.db')

def add_user(u, p):
    conn = get_db()
    try:
        conn.execute("INSERT INTO users VALUES (?, ?)", (u, p))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

# --- واجهة المستخدم ---
st.set_page_config(page_title="DARK NET | GLOBAL ARCHIVE", layout="wide")
st_autorefresh(interval=3000, key="sync")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New'; }
    .stButton>button { width: 100%; background-color: #1a0000; color: #ff0000; border: 1px solid #ff0000; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; color: black; box-shadow: 0px 0px 15px #ff0000; }
    .stTextInput>div>div>input { background-color: #000; color: #00ff00 !important; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #000; border-right: 2px solid #ff0000; }
    .css-17l69k3 { background: #000; }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- بوابة الدخول ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔴 DARK NET TERMINAL</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["ENTRY", "NEW IDENTITY"])
    with t1:
        u = st.text_input("ID")
        p = st.text_input("KEY", type="password")
        if st.button("CONNECT"):
            conn = get_db()
            user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
            if user:
                st.session_state.logged_in, st.session_state.username = True, u
                st.rerun()
            else: st.error("INVALID ACCESS")
    with t2:
        nu = st.text_input("CREATE ID")
        np = st.text_input("CREATE KEY", type="password")
        if st.button("GENERATE"):
            if add_user(nu, np):
                st.session_state.logged_in, st.session_state.username = True, nu
                st.rerun()
    st.stop()

# --- القائمة الجانبية (التحكم) ---
with st.sidebar:
    st.title(f"💀 {st.session_state.username}")
    
    # 1. إنشاء قناة (أكثر من عضو)
    with st.expander("📁 تأسيس مجموعة (قناة)"):
        g_name = st.text_input("اسم المجموعة")
        members = st.text_input("الأعضاء (افصل بفاصلة ,)")
        if st.button("تأكيد التأسيس"):
            sid = str(uuid.uuid4())[:8]
            inv_code = str(uuid.uuid4())[:5].upper()
            conn = get_db()
            conn.execute("INSERT INTO servers VALUES (?, ?, ?, ?)", (sid, g_name, st.session_state.username, inv_code))
            conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, st.session_state.username))
            for m in members.split(','):
                conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, m.strip()))
            conn.commit()
            st.success(f"تم! كود الدعوة: {inv_code}")
            st.rerun()

    # 2. انضمام بكود دعوة
    with st.expander("🔑 انضمام عبر كود دعوة"):
        code = st.text_input("أدخل الكود")
        if st.button("اختراق القناة"):
            conn = get_db()
            serv = conn.execute("SELECT id FROM servers WHERE invite_code=?", (code,)).fetchone()
            if serv:
                conn.execute("INSERT OR IGNORE INTO server_members VALUES (?, ?)", (serv[0], st.session_state.username))
                conn.commit()
                st.success("تم الانضمام!")
                st.rerun()

    # 3. رسالة خاصة (Direct Message)
    with st.expander("✉️ رسالة خاصة (DM)"):
        target_dm = st.text_input("يوزر الشخص")
        if st.button("فتح اتصال"):
            # صنع ID فريد للمحادثة الخاصة بين الاثنين
            dm_id = "".join(sorted([st.session_state.username, target_dm]))
            st.session_state.active_sid = dm_id
            st.session_state.active_name = f"Private: {target_dm}"
            st.rerun()

    st.divider()
    
    # قائمة القنوات والرسائل
    conn = get_db()
    my_servs = conn.execute("SELECT s.id, s.name, s.invite_code FROM servers s JOIN server_members sm ON s.id = sm.server_id WHERE sm.username=?", (st.session_state.username,)).fetchall()
    
    st.markdown("### 🛰️ قنواتك")
    if st.button("📢 الساحة العامة"): 
        st.session_state.active_sid = "PUBLIC"
        st.session_state.active_name = "الساحة العامة"
    
    for s in my_servs:
        if st.button(f"👁️ {s[1]} (Code: {s[2]})"):
            st.session_state.active_sid = s[0]
            st.session_state.active_name = s[1]

# --- منطقة الدردشة ---
if "active_sid" not in st.session_state:
    st.session_state.active_sid = "PUBLIC"
    st.session_state.active_name = "الساحة العامة"

st.title(f"📡 {st.session_state.active_name}")

# عرض الرسائل
conn = get_db()
msgs = conn.execute("SELECT sender, content, type FROM messages WHERE server_id=? ORDER BY timestamp ASC", (st.session_state.active_sid,)).fetchall()
for m in msgs:
    with st.chat_message("user"):
        st.write(f"**[{m[0]}]**")
        if m[2] == "text": st.code(m[1], language=None)
        else: st.image(m[1])

# إرسال البيانات
p = st.chat_input("أرسل بيانات مشفرة...")
img = st.sidebar.file_uploader("🖼️ رفع وثيقة", type=['png','jpg'])

if p:
    conn = get_db()
    conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, p, "text"))
    conn.commit()
    st.rerun()

if img:
    if st.sidebar.button("نشر الصورة"):
        buf = io.BytesIO()
        Image.open(img).save(buf, format="PNG")
        istr = base64.b64encode(buf.getvalue()).decode()
        conn = get_db()
        conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, istr, "image"))
        conn.commit()
        st.rerun()
