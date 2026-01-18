import streamlit as st
import pandas as pd
import requests
import time
import base64

# --- הגדרות עמוד (חובה בהתחלה) ---
st.set_page_config(
    page_title="מערכת שו\"ב - חילוץ והצלה",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed" # סוגר תפריט צד כדי לחסוך מקום
)

# --- CSS עיצוב צפוף (ללא גלילה) ---
st.markdown("""
<style>
    .stApp { direction: rtl; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; } /* הקטנת שוליים */
    div[data-testid="column"] { background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 1px solid #d1d5db; }
    h3 { margin-top: 0; font-size: 1.1rem; }
    p, span { font-size: 0.9rem; }
    .stButton button { width: 100%; }
    
    /* עיצוב התראת צבע אדום */
    .red-alert {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        animation: blinker 1s linear infinite;
        text-align: center;
        font-weight: bold;
    }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- פונקציות שירות (API) ---

def get_weather(location="Ness Ziona"):
    """שליפת מזג אוויר מ-wttr.in כפי שביקשת"""
    try:
        # פורמט j1 נותן JSON נקי
        url = f"https://wttr.in/{location}?format=j1&lang=he"
        response = requests.get(url, timeout=5)
        data = response.json()
        current = data['current_condition'][0]
        temp = current['temp_C']
        desc = current['lang_he'][0]['value']
        
        # לוגיקת מזג אוויר קיצוני (שיחזור מהאפיון שלך)
        alert = None
        temp_val = int(temp)
        if temp_val > 35: alert = "🔥 עומס חום קיצוני"
        elif temp_val < 5: alert = "❄️ קרה / קיפאון"
        elif "rain" in desc.lower() or "גשם" in desc: alert = "🌧️ סכנת החלקה/הצפות"
        
        return temp, desc, alert
    except:
        return "N/A", "תקלה במשיכת נתונים", None

def check_red_alerts():
    """סימולציה של בדיקת צבע אדום (ה-API האמיתי של פיקוד העורף חסום לרוב שרתים)"""
    # כאן אני מדמה מצב כדי שתראה איך המערכת מגיבה.
    # במבצעי אמיתי נחליף ל-API הרשמי עם Proxy.
    return {
        "active": False, # שנה ל-True כדי לבדוק את הסירנה
        "locations": ["אשקלון", "זיקים"],
        "time_to_shelter": "15 שניות"
    }

def play_siren():
    """ניגון סירנה (צליל בסיסי)"""
    # הטמעת סאונד ב-HTML כדי לעקוף מגבלות דפדפן
    audio_html = """
    <audio autoplay>
    <source src="https://upload.wikimedia.org/wikipedia/commons/e/e0/Air_Raid_Siren_Traffic_US.ogg" type="audio/ogg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- אתחול נתונים ---
if 'df_anchor' not in st.session_state:
    st.session_state.df_anchor = pd.DataFrame([
        ["1", "קומה 3", "ישראל ישראלי", "לכוד", "050-0000000"],
        ["2", "חניון", "פלוני אלמוני", "נעדר", "052-1111111"],
    ], columns=["מס\"ד", "מיקום", "שם", "סטטוס", "טלפון"])

# --- בניית המסך (Grid Layout - הכל במסך אחד) ---

# שורה עליונה: כותרת + סטטוס חירום
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.title("מערכת שו\"ב - חילוץ והצלה")
with top_col2:
    if st.button("🔄 רענן נתונים"):
        st.rerun()

st.markdown("---")

# גריד ראשי - חלוקה ל-3 עמודות כדי למנוע גלילה
col_weather, col_alerts, col_tools = st.columns(3)

# 1. קוביית מזג אוויר
with col_weather:
    st.subheader("🌤️ מזג אוויר (נס ציונה)")
    temp, desc, weather_alert = get_weather()
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="טמפרטורה", value=f"{temp}°C")
    with c2:
        st.write(f"**{desc}**")
    
    if weather_alert:
        st.error(f"{weather_alert}")
    else:
        st.success("תנאים נוחים לפעילות")

# 2. קוביית פיקוד העורף והתראות
with col_alerts:
    st.subheader("📢 התראות וזמני התגוננות")
    alerts = check_red_alerts()
    
    if alerts["active"]:
        st.markdown(f'<div class="red-alert">🚨 צבע אדום פעיל! 🚨<br>{", ".join(alerts["locations"])}</div>', unsafe_allow_html=True)
        st.write(f"**זמן כניסה למרחב מוגן:** {alerts['time_to_shelter']}")
        play_siren() # הפעלת סירנה
    else:
        st.info("🟢 שיגרה - אין התראות פעילות")
        st.caption("מדיניות התגוננות: ירוק (מלאה)")

# 3. כלים מהירים
with col_tools:
    st.subheader("🛠️ כלים מהירים")
    st.button("🔦 הפעל תאורת חירום (סימולציה)")
    st.button("📞 חייג למוקד 104")

# שורה תחתונה: טבלת עוגן (תופסת את רוב המסך)
st.markdown("### 📋 תמונת מצב לכודים ונעדרים")
edited_df = st.data_editor(
    st.session_state.df_anchor,
    num_rows="dynamic",
    use_container_width=True,
    height=300 # גובה מקובע למניעת גלילה של כל העמוד
)
st.session_state.df_anchor = edited_df
