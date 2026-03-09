import streamlit as st
from streamlit_autorefresh import st_autorefresh
from PIL import Image
import sqlite3
import hashlib
import io

# --- إعداد قاعدة البيانات (الأرشفة الأبدية) ---
def init_db():
    conn = sqlite3.connect('dark_net.db')
    c = conn.cursor()
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    # جدول السيرفرات
    c.execute('''CREATE TABLE IF NOT EXISTS servers (id TEXT PRIMARY KEY, name TEXT, creator TEXT)''')
    # جدول أعضاء السيرفرات
    c.execute('''CREATE TABLE IF NOT EXISTS server_members (server_id TEXT, username TEXT)''')
    # جدول الرسائل (نص وصور)
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 server_id TEXT, sender TEXT, content TEXT, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# --- دالات التعامل مع البيانات ---
def add_user(u, p):
    conn = sqlite3.connect('dark_net.db')
    try:
        conn.execute("INSERT INTO users VALUES (?, ?)", (u, p))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def check_user(u, p):
    conn = sqlite3.connect('dark_net.db')
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
    conn.close()
    return user

# --- إعدادات الواجهة ---
st.set_page_config(page_title="DARK NET | PERSISTENT ARCHIVE", layout="wide")
st_autorefresh(interval=4000, key="db_sync")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Courier New'; text-shadow: 2px 2px #330000; }
    .stButton>button { width: 100%; background-color: #1a0000; color: #ff0000; border: 1px solid #ff0000; }
    .stButton>button:hover { background-color: #ff0000; color: black; box-shadow: 0px 0px 15px #ff0000; }
    .stTextInput>div>div>input { background-color: #000; color: #00ff00 !important; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #000; border-right: 1px solid #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- منطق الدخول والتسجيل ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔴 DARK NET ENTRANCE</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 JOIN THE ORGANIZATION"])
    
    with tab1:
        u = st.text_input("IDENTITY CODE")
        p = st.text_input("PASSKEY", type="password")
        if st.button("AUTHORIZE ACCESS"):
            if check_user(u, p):
                st.session_state.logged_in, st.session_state.username = True, u
                st.rerun()
            else: st.error("ACCESS DENIED")

    with tab2:
        new_u = st.text_input("NEW IDENTITY CODE")
        new_p = st.text_input("NEW PASSKEY", type="password")
        if st.button("INITIALIZE REGISTRATION"):
            if new_u and new_p:
                if add_user(new_u, new_p):
                    # تسجيل دخول تلقائي فور الإنشاء
                    st.session_state.logged_in, st.session_state.username = True, new_u
                    st.success("Identity Created. Accessing Mainframe...")
                    time.sleep(1)
                    st.rerun()
                else: st.error("Identity Code already exists in the archives.")
    st.stop()

# --- القائمة الجانبية وإدارة السيرفرات ---
with st.sidebar:
    st.markdown(f"### 💀 العميل: {st.session_state.username}")
    if st.button("🔴 تدمير الجلسة (Logout)"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.divider()
    
    # إنشاء سيرفر جديد
    with st.expander("➕ تأسيس قناة سرية"):
        s_name = st.text_input("اسم القناة")
        target = st.text_input("يوزر العميل المستهدف")
        if st.button("تأكيد التأسيس"):
            import uuid
            s_id = str(uuid.uuid4())[:8]
            conn = sqlite3.connect('dark_net.db')
            conn.execute("INSERT INTO servers VALUES (?, ?, ?)", (s_id, s_name, st.session_state.username))
            conn.execute("INSERT INTO server_members VALUES (?, ?)", (s_id, st.session_state.username))
            conn.execute("INSERT INTO server_members VALUES (?, ?)", (s_id, target))
            conn.commit()
            conn.close()
            st.success("تم تأسيس القناة")
            st.rerun()

    st.divider()
    # جلب السيرفرات الخاصة بالعميل
    conn = sqlite3.connect('dark_net.db')
    my_servs = conn.execute("""SELECT servers.id, servers.name FROM servers 
                               JOIN server_members ON servers.id = server_members.server_id 
                               WHERE server_members.username = ?""", (st.session_state.username,)).fetchall()
    conn.close()

    options = ["الساحة العامة"] + [f"{s[1]} ({s[0]})" for s in my_servs]
    choice = st.radio("اختر قناة الاتصال:", options)
    
    selected_sid = "PUBLIC" if choice == "الساحة العامة" else choice.split('(')[-1].strip(')')

# --- نظام المحادثة المتقدم ---
st.title(f"🕸️ ARCHIVE: {choice}")

# جلب الرسائل من قاعدة البيانات
conn = sqlite3.connect('dark_net.db')
msgs = conn.execute("SELECT sender, content, type FROM messages WHERE server_id=? ORDER BY timestamp ASC", (selected_sid,)).fetchall()
conn.close()

for m in msgs:
    with st.chat_message("user"):
        st.write(f"**[{m[0]}]**")
        if m[2] == "text": st.code(m[1], language=None)
        else: st.image(m[1])

# منطقة الإرسال
prompt = st.chat_input("أدخل البيانات...")
img_file = st.sidebar.file_uploader("📤 رفع وثيقة (صورة)", type=['png', 'jpg'])

if prompt:
    conn = sqlite3.connect('dark_net.db')
    conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", 
                 (selected_sid, st.session_state.username, prompt, "text"))
    conn.commit()
    conn.close()
    st.rerun()

if img_file:
    if st.sidebar.button("إرسال الصورة"):
        # تحويل الصورة لـ Base64 لتخزينها في قاعدة البيانات
        img = Image.open(img_file)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        conn = sqlite3.connect('dark_net.db')
        conn.execute("INSERT INTO messages (server_id, sender, content, type) VALUES (?, ?, ?, ?)", 
                     (selected_sid, st.session_state.username, img_str, "image"))
        conn.commit()
        conn.close()
        st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #1a1a1a;'>DATABASE STATUS: SECURED & PERSISTENT</p>", unsafe_allow_html=True)
