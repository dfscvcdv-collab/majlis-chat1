import streamlit as st
import random

# إعدادات الصفحة
st.set_page_config(page_title="لعبة التخمين السرية", page_icon="🕵️‍♂️")

# تنسيق CSS عشان يطلع الشكل "أحلى" ومناسب للجوال
st.markdown("""
    <style>
    .main { background-color: #121212; }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #6200ee;
        color: white;
    }
    .secret-box {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #03dac6;
    }
    </style>
    """, unsafe_allow_index=True)

# إدارة حالة اللعبة (State)
if 'stage' not in st.session_state:
    st.session_state.stage = 'setup'
    st.session_state.players_data = []
    st.session_state.current_idx = 0

# --- المرحلة 1: الإعداد ---
if st.session_state.stage == 'setup':
    st.title("🕵️‍♂️ لعبة التخمين")
    
    range_choice = st.selectbox("اختر نطاق الأرقام:", ["0 - 100", "0 - 1000", "500 - 1000", "100 - 1000"])
    names_input = st.text_input("أدخل أسماء اللاعبين (افصل بينهم بفاصلة):", placeholder="عبود، فيصل، خالد")
    
    if st.button("ابدأ اللعب"):
        if names_input:
            # معالجة النطاق
            if range_choice == "0 - 100": r_min, r_max = 0, 100
            elif range_choice == "0 - 1000": r_min, r_max = 0, 1000
            elif range_choice == "500 - 1000": r_min, r_max = 500, 1000
            else: r_min, r_max = 100, 1000
            
            # توزيع الأرقام
            names = [n.strip() for n in names_input.replace("،", ",").split(",") if n.strip()]
            st.session_state.players_data = [{"name": name, "number": random.randint(r_min, r_max)} for name in names]
            st.session_state.stage = 'distribute'
            st.rerun()
        else:
            st.error("يا وحش سجل الأسماء أول!")

# --- المرحلة 2: توزيع الأرقام ---
elif st.session_state.stage == 'distribute':
    idx = st.session_state.current_idx
    if idx < len(st.session_state.players_data):
        player = st.session_state.players_data[idx]
        
        st.subheader(f"دور اللاعب: {player['name']}")
        st.info("عط الجوال لراعي الاسم المكتوب فوق.")
        
        if st.checkbox(f"أنا {player['name']}.. ورني رقمي"):
            st.markdown(f"""
            <div class="secret-box">
                <p>رقمك السري هو:</p>
                <h1 style="color: #03dac6;">{player['number']}</h1>
                <p>احفظ الرقم ولا تعلم أحد!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("حفظت الرقم، للي بعده"):
                st.session_state.current_idx += 1
                st.rerun()
    else:
        st.session_state.stage = 'play'
        st.rerun()

# --- المرحلة 3: شاشة اللعب والأسئلة ---
elif st.session_state.stage == 'play':
    st.title("🎮 بدأت اللعبة!")
    st.success("كل واحد الحين يعرف رقمه.. ابدأوا التحدي!")
    
    st.write("### اللاعبين المشاركين:")
    for p in st.session_state.players_data:
        st.write(f"- {p['name']}")
        
    st.divider()
    st.write("الآن فلان يسأل علان.. حاولوا تخمنون الأرقام!")
    
    if st.button("إعادة اللعبة"):
        st.session_state.clear()
        st.rerun()
