import streamlit as st
import sqlite3
import requests
from datetime import datetime
from PIL import Image
import os

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect('child_safety.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age TEXT,
    touch_type TEXT,
    emotion TEXT,
    location TEXT,
    support_assigned TEXT,
    time TEXT
)
''')

conn.commit()

# ---------------- SUPPORT NETWORK ---------------- #

support_db = {
    "Delhi": {"psychologist": "Dr. Meera", "lawyer": "Adv. Rahul", "volunteer": "Team Delhi"},
    "Noida": {"psychologist": "Dr. Neha", "lawyer": "Adv. Aman", "volunteer": "Team Noida"},
    "Other": {"psychologist": "Dr. Help", "lawyer": "Legal Aid", "volunteer": "Support Team"}
}

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="Child Safety Platform", layout="wide")

st.title("🛡️ Child Safety & Support Platform")
st.write("You are safe here ❤️")

menu = st.sidebar.selectbox(
    "Menu",
    ["Report", "🚨 Panic", "Chat Support", "Education", "Parent Guide"]
)

# ---------------- LOCATION FUNCTION ---------------- #

def get_location():
    try:
        res = requests.get("https://ipinfo.io").json()
        city = res.get("city", "")
        country = res.get("country", "")
        return f"{city}, {country}"
    except:
        return "Location not found"

# ---------------- IMAGE LOADER ---------------- #

def load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    else:
        return None

# ---------------- REPORT PAGE ---------------- #

if menu == "Report":

    st.header("Tell Us What Happened")

    age = st.text_input("Your Age (optional)")

    col1, col2, col3 = st.columns(3)

    good_img = load_image("images/good_touch.png")
    bad_img = load_image("images/bad_touch.png")
    unsafe_img = load_image("images/unsafe_touch.png")

    with col1:
        if good_img:
            st.image(good_img, caption="Good Touch")

    with col2:
        if bad_img:
            st.image(bad_img, caption="Bad Touch")

    with col3:
        if unsafe_img:
            st.image(unsafe_img, caption="Unsafe Touch")

    touch_type = st.radio(
        "Select what happened",
        ["Good Touch", "Bad Touch", "Unsafe / Confusing Touch"]
    )

    emotion = st.radio(
        "How are you feeling?",
        ["😢 Sad", "😨 Scared", "😡 Angry", "😔 Confused", "😊 Okay"]
    )

    region = st.text_input("Your City")

    if st.button("Submit Report"):

        region_key = region if region in support_db else "Other"
        support = support_db[region_key]

        c.execute(
            "INSERT INTO reports(age,touch_type,emotion,location,support_assigned,time) VALUES(?,?,?,?,?,?)",
            (
                age,
                touch_type,
                emotion,
                region,
                str(support),
                datetime.now()
            )
        )
        conn.commit()

        st.success("Report submitted ❤️")
        st.info(f"Support Assigned: {support}")

# ---------------- PANIC BUTTON ---------------- #

elif menu == "🚨 Panic":

    st.header("Emergency Help")

    st.error("Press if you are in danger")

    if st.button("🚨 PANIC - I NEED HELP"):

        location = get_location()

        st.warning("Alert sent to emergency team!")
        st.write("📍 Your Location:", location)

        st.success("Nearby volunteers notified")
        st.info("Go to a safe place near trusted adult")

# ---------------- CHATBOT ---------------- #

elif menu == "Chat Support":

    st.header("Talk to Support Bot")

    user_input = st.text_input("Type your message")

    if user_input:

        msg = user_input.lower()

        if "scared" in msg or "dar" in msg:
            response = "I understand you are scared. You are safe here. Do you want to tell me what happened?"
        elif "help" in msg:
            response = "I am here to help you. You can press panic button or report safely."
        elif "touch" in msg:
            response = "If someone touched you and you feel uncomfortable, it is not your fault."
        else:
            response = "You are brave for sharing ❤️"

        st.write("Support Bot:", response)

# ---------------- EDUCATION ---------------- #

elif menu == "Education":

    st.header("Good Touch vs Bad Touch")

    st.image("images/good_touch.png", caption="Good Touch")
    st.image("images/bad_touch.png", caption="Bad Touch")

    st.write("""
    ✅ Good Touch:
    - Makes you feel safe
    - Caring hug from parents

    ❌ Bad Touch:
    - Private parts touch
    - Makes you uncomfortable
    - Asked to keep secret
    """)

    st.write("""
    Safety Rule:
    SAY NO → RUN → TELL
    """)

# ---------------- PARENT GUIDE ---------------- #

elif menu == "Parent Guide":

    st.header("For Parents & Teachers")

    st.write("""
    • Teach body boundaries  
    • Encourage open communication  
    • Believe the child  
    • Seek professional help  
    """)

    st.info("Child safety is everyone's responsibility ❤️")

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("This platform provides safe reporting support.")
