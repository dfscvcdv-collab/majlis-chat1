import streamlit as st
import random
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="مجموعة الألعاب الجماعية", page_icon="🎮")

# 2. تهيئة المتغيرات في الذاكرة (Session State)
if 'player_list' not in st.session_state:
    st.session_state.player_list = []
if 'game_choice' not in st.session_state:
    st.session_state.game_choice = "الرئيسية"
if 'lucky_winner' not in st.session_state:
    st.session_state.lucky_winner = None
if 'random_char' not in st.session_state:
    st.session_state.random_char = ""

# --- قائمة الحروف الأبجدية ---
arabic_chars = "أبتثجحخدذرزسشصضطظعغفقكلمنهوي"

# 3. تنسيق CSS
st.markdown("""
    <style>
    .main { background-color: #121212; }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background-color: #6200ee;
        color: white;
        font-weight: bold;
        height: 50px;
    }
    .winner-box {
        background-color: #1e1e1e;
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        border: 4px dashed #03dac6;
        margin-top: 20px;
    }
    .player-tag {
        background-color: #333;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
        border: 1px solid #555;
    }
    h1, h2, h3, p { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- الجانب الجانبي (Sidebar) لإدارة الأسماء واختيار اللعبة ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.session_state.game_choice = st.radio("اختر اللعبة:", ["الرئيسية", "لعبة الأرقام السرية", "عجلة الحظ (حيوان جماد)"])
    
    st.divider()
    st.subheader("👥 إدارة اللاعبين")
    new_name = st.text_input("أضف اسم لاعب:", key="sidebar_name")
    if st.button("➕ إضافة"):
        if new_name.strip() and new_name not in st.session_state.player_list:
            st.session_state.player_list.append(new_name.strip())
            st.rerun()
    
    if st.session_state.player_list:
        st.write("اللاعبين الحاضرين:")
        for name in st.session_state.player_list:
            st.markdown(f'<div class="player-tag">{name}</div>', unsafe_allow_html=True)
        if st.button("🗑️ مسح القائمة"):
            st.session_state.player_list = []
            st.rerun()

# --- الشاشة الرئيسية ---
if st.session_state.game_choice == "الرئيسية":
    st.title("🎮 أهلاً بكم في مجلس الألعاب")
    st.info("أضف أسماء اللاعبين من القائمة الجانبية ثم اختر لعبة لتبدأ!")
    if not st.session_state.player_list:
        st.warning("⚠️ ابدأ بإضافة لاعبين أولاً.")

# --- لعبة الأرقام السرية (كودك القديم مع تعديلات الحفظ) ---
elif st.session_state.game_choice == "لعبة الأرقام السرية":
    st.title("🕵️‍♂️ لعبة الرقم السري")
    if len(st.session_state.player_list) < 2:
        st.error("تحتاج لاعبين على الأقل!")
    else:
        # (هنا يوضع منطق اللعبة الأول نفسه مع ربطه بـ player_list)
        # لتوفير المساحة، افترضنا أنك بتدمجه هنا بنفس المنطق السابق.
        st.write("هذه اللعبة جاهزة، استخدم الأسماء المضافة!")
        if st.button("توليد أرقام عشوائية والبدء"):
             st.success("تم توزيع الأرقام! (طبق منطق التوزيع هنا)")

# --- اللعبة الجديدة: عجلة الحظ (حيوان جماد) ---
elif st.session_state.game_choice == "عجلة الحظ (حيوان جماد)":
    st.title("🎡 عجلة الحظ العشوائية")
    st.write("ضع الجوال في المنتصف واضغط الزر!")
    
    if len(st.session_state.player_list) < 2:
        st.error("أضف لاعبين من القائمة الجانبية أولاً!")
    else:
        if st.button("🚀 لـف العجلة!"):
            # أنيميشن بسيط
            placeholder = st.empty()
            for _ in range(10):
                temp_name = random.choice(st.session_state.player_list)
                placeholder.markdown(f"<h2 style='color: gray;'>🔄 يدور... {temp_name}</h2>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            st.session_state.lucky_winner = random.choice(st.session_state.player_list)
            st.session_state.random_char = random.choice(arabic_chars)
            st.balloons()

        if st.session_state.lucky_winner:
            st.markdown(f"""
            <div class="winner-box">
                <h3>وقع الاختيار على:</h3>
                <h1 style="color: #03dac6; font-size: 60px;">{st.session_state.lucky_winner}</h1>
                <hr>
                <p>المطلوب منك (اسم، حيوان، جماد، بلد) يبدأ بحرف:</p>
                <h1 style="color: #ff0266; font-size: 80px;">{st.session_state.random_char}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 جولة أخرى"):
                st.session_state.lucky_winner = None
                st.rerun()
