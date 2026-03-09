import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import sqlite3
import uuid
import io
import base64

# --- إعداد قاعدة البيانات v4 ---
def init_db():
    conn = sqlite3.connect('dark_net_v4.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS servers (id TEXT PRIMARY KEY, name TEXT, creator TEXT, invite_code TEXT, type TEXT DEFAULT "GROUP")')
    c.execute('CREATE TABLE IF NOT EXISTS server_members (server_id TEXT, username TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, server_id TEXT, sender TEXT, content TEXT, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()
def get_db(): return sqlite3.connect('dark_net_v4.db')

# --- التصميم الفخم ---
st.set_page_config(page_title="DARK NET | PRIVATE COMMS", layout="wide")
st_autorefresh(interval=3000, key="global_sync")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New'; }
    .stButton>button { width: 100%; background-color: #1a0000; color: #ff0000; border: 1px solid #ff0000; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000 !important; color: black !important; box-shadow: 0px 0px 10px #ff0000; }
    .stTextInput>div>div>input { background-color: #000; color: #00ff00 !important; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #000; border-right: 2px solid #ff0000; }
    .member-tag { padding: 4px 8px; border: 1px solid #ff0000; color: #ff0000; border-radius: 4px; margin: 2px; display: inline-block; font-size: 11px; background: #1a0000; }
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
            if conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone():
                st.session_state.logged_in, st.session_state.username = True, u
                st.rerun()
            else: st.error("ACCESS DENIED")
    with t2:
        nu = st.text_input("NEW ID")
        np = st.text_input("NEW KEY", type="password")
        if st.button("GENERATE"):
            if nu and np:
                conn = get_db()
                if conn.execute("SELECT username FROM users WHERE username=?", (nu,)).fetchone():
                    st.error("Identity Taken")
                else:
                    conn.execute("INSERT INTO users VALUES (?, ?)", (nu, np))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.username = True, nu
                    st.rerun()
    st.stop()

# --- القائمة الجانبية (الأدوات السريّة) ---
with st.sidebar:
    st.title(f" {st.session_state.username}")
    
    # 1. المجموعات
    with st.expander(" تأسيس مجموعة (Group)"):
        g_name = st.text_input("اسم المجموعة")
        m_list = st.text_input("الأعضاء (فاصلة بينهم)")
        if st.button("تأسيس Group"):
            sid, inv = str(uuid.uuid4())[:8], str(uuid.uuid4())[:5].upper()
            conn = get_db()
            conn.execute("INSERT INTO servers VALUES (?, ?, ?, ?, 'GROUP')", (sid, g_name, st.session_state.username, inv))
            conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, st.session_state.username))
            for m in m_list.split(','):
                if m.strip(): conn.execute("INSERT INTO server_members VALUES (?, ?)", (sid, m.strip()))
            conn.commit()
            st.success(f"Group Created! Code: {inv}")
            st.rerun()

    # 2. الانضمام عبر كود (الميزة المطلوبة)
    with st.expander(" انضمام عبر كود مشفر"):
        inv_input = st.text_input("أدخل كود القناة")
        if st.button("تفعيل الكود"):
            conn = get_db()
            server_to_join = conn.execute("SELECT id, name FROM servers WHERE invite_code = ?", (inv_input.upper(),)).fetchone()
            if server_to_join:
                conn.execute("INSERT OR IGNORE INTO server_members VALUES (?, ?)", (server_to_join[0], st.session_state.username))
                conn.commit()
                st.success(f"تم : {server_to_join[1]}")
                st.rerun()
            else:
                st.error("الكود غير صالح أو منتهي")

    # 3. الخاص (Private DM)
    with st.expander(" فتح اتصال خاص (DM)"):
        target_user = st.text_input("يوزر العميل")
        if st.button("بدء التشفير الثنائي"):
            conn = get_db()
            if conn.execute("SELECT username FROM users WHERE username=?", (target_user,)).fetchone():
                dm_id = "DM-" + "-".join(sorted([st.session_state.username, target_user]))
                conn.execute("INSERT OR IGNORE INTO servers (id, name, creator, type) VALUES (?, ?, ?, 'DM')", (dm_id, f"Direct: {target_user}", "SYSTEM"))
                conn.execute("INSERT OR IGNORE INTO server_members VALUES (?, ?)", (dm_id, st.session_state.username))
                conn.execute("INSERT OR IGNORE INTO server_members VALUES (?, ?)", (dm_id, target_user))
                conn.commit()
                st.session_state.active_sid = dm_id
                st.session_state.active_name = f" محادثة خاصة مع {target_user}"
                st.rerun()
            else: st.error("العميل غير موجود")

    st.divider()
    
    conn = get_db()
    my_channels = conn.execute("""SELECT s.id, s.name, s.type, s.invite_code FROM servers s 
                                  JOIN server_members sm ON s.id = sm.server_id 
                                  WHERE sm.username = ?""", (st.session_state.username,)).fetchall()
    
    st.markdown("###  قنوات الاتصال")
    if st.button(" الساحة العامة"):
        st.session_state.active_sid, st.session_state.active_name = "PUBLIC", "الساحة العامة"

    for c in my_channels:
        # عرض الكود بجانب اسم القناة للمالك لسهولة الإرسال
        label = f"👥 {c[1]} [{c[3]}]" if c[2] == 'GROUP' else f"✉️ {c[1]}"
        if st.button(label):
            st.session_state.active_sid, st.session_state.active_name = c[0], c[1]

# --- منطقة المحادثة ---
if "active_sid" not in st.session_state:
    st.session_state.active_sid, st.session_state.active_name = "PUBLIC", "الساحة العامة"

st.title(f" {st.session_state.active_name}")

if "DM-" not in st.session_state.active_sid and st.session_state.active_sid != "PUBLIC":
    conn = get_db()
    m_data = conn.execute("SELECT username FROM server_members WHERE server_id=?", (st.session_state.active_sid,)).fetchall()
    st.markdown(" ".join([f"<span class='member-tag'>● {m[0]}</span>" for m in m_data]), unsafe_allow_html=True)

conn = get_db()
msgs = conn.execute("SELECT sender, content, type FROM messages WHERE server_id=? ORDER BY timestamp ASC", (st.session_state.active_sid,)).fetchall()
for m in msgs:
    with st.chat_message("user"):
        st.write(f"**[{m[0]}]**")
        if m[2] == "text": st.code(m[1], language=None)
        else: st.image(m[1])

prompt = st.chat_input(" رسالة...")
img_file = st.sidebar.file_uploader("📤 رفع صور", type=['png','jpg'])

if prompt:
    conn = get_db()
    conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, prompt, "text"))
    conn.commit()
    st.rerun()

if img_file:
    if st.sidebar.button("نشر الصورة"):
        buf = io.BytesIO()
        Image.open(img_file).save(buf, format="PNG")
        istr = base64.b64encode(buf.getvalue()).decode()
        conn = get_db()
        conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", (st.session_state.active_sid, st.session_state.username, istr, "image"))
        conn.commit()
        st.rerun()
