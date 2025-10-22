# ui/app.py
import os
import time
import random
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd

# --- FOOTER STYLING (OrbyAI theme) ---
footer_style = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: linear-gradient(90deg, #0a0f29 0%, #1b2a5b 100%);
        color: #c9d1f2;
        text-align: center;
        font-size: 14px;
        padding: 10px 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.3px;
        font-family: 'Inter', sans-serif;
        z-index: 100;
    }
    .footer a {
        color: #6ea8fe;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
"""
st.markdown(footer_style, unsafe_allow_html=True)


# --------------------
# Page config
# --------------------
st.set_page_config(page_title="AI Buddy • OrbyAI", page_icon="🤝", layout="wide")

# --------------------
# Helpers
# --------------------
def safe_logo(path: str, width: int = 120):
    try:
        if os.path.exists(path):
            st.image(path, width=width)
    except Exception:
        pass  # never break UI due to image issues

def seed_calendar(days=5):
    now = datetime.now()
    rows = []
    for i in range(days):
        day = now + timedelta(days=i)
        if random.random() > 0.35:
            rows.append(
                {
                    "Date": day.date().isoformat(),
                    "Event": random.choice(
                        ["Team Sync", "Client Call", "Deep Work", "Well-being Break"]
                    ),
                    "Location": random.choice(["Zoom", "Room 2A", "Remote", "Office"]),
                }
            )
    return pd.DataFrame(rows)

def seed_emails(n=6):
    senders = ["ansia@gmail.com", "aditi@gmail.com", "zena@gmail.ai", "vrushti@gmail.com"]
    subjects = ["Follow-up on project", "Reminder: Wellness Friday", "Presentation Preperation", "Weekly report"]
    return pd.DataFrame(
        {
            "From": random.choices(senders, k=n),
            "Subject": random.choices(subjects, k=n),
            "Priority": random.choices(["High", "Medium", "Low"], k=n),
        }
    )

# --------------------
# Emoji micro-animations (CSS)
# --------------------
ANIM_CSS = """
<style>
.pulse { display:inline-block; animation:pulse 1.2s infinite; }
@keyframes pulse {
  0% { transform: scale(1); }
  50%{ transform: scale(1.15); }
  100%{ transform: scale(1); }
}
.wave { display:inline-block; transform-origin: 70% 70%; animation: wave 1.6s infinite; }
@keyframes wave {
  0% { transform: rotate(0deg) }
  10% { transform: rotate(14deg) }
  20% { transform: rotate(-8deg) }
  30% { transform: rotate(14deg) }
  40% { transform: rotate(-4deg) }
  50% { transform: rotate(10deg) }
  60% { transform: rotate(0deg) }
  100% { transform: rotate(0deg) }
}
</style>
"""
st.markdown(ANIM_CSS, unsafe_allow_html=True)

# --------------------
# Sidebar
# --------------------
with st.sidebar:
    safe_logo("assets/ai_buddy_logo.png", width=100)
    st.title("AI Buddy Navigation")
    st.markdown("### 🤝 Your Proactive Personal Companion")

    # Wellness mode toggle
    wellness_mode = st.toggle(
        "Enable Wellness Mode",
        value=st.session_state.get("wellness_mode", True),
        help="When on, AI Buddy uses empathetic static replies for emotional inputs even without API calls.",
    )
    st.session_state.wellness_mode = wellness_mode

    nav = st.radio("Navigate:", ["Home", "Chat", "Calendar", "Mail", "Deliverables", "Approvals", "Support", "Settings"])


# --------------------
# State
# --------------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "play_music" not in st.session_state:
    st.session_state.play_music = False
if "connect_friend" not in st.session_state:
    st.session_state.connect_friend = False

# --------------------
# Smart Mood Replies
# --------------------
def get_static_reply(prompt: str, wellness_enabled: bool = True):
    """Return (reply_text, flags_dict) or (None, {}) if no static match."""
    text = (prompt or "").strip().lower()
    flags = {"play_music": False, "connect_friend": False}

    if any(w in text for w in ["hi", "hello", "hey", "yo", "hola"]):
        return (
            "👋 <span class='wave'>Hey</span> there! How are you doing today? "
            "Hope your day’s off to a great start ☀️",
            flags,
        )

    if wellness_enabled:
        if any(w in text for w in ["sad", "lonely", "upset", "feeling low", "depressed"]):
            flags["play_music"] = True
            flags["connect_friend"] = True
            return (
                "💙 I’m really sorry you’re feeling that way. I’m here for you. "
                "We can talk it through, listen to some <span class='pulse'>🎵</span> uplifting music, "
                "or I can help you connect with a friend 💌.",
                flags,
            )

        if any(w in text for w in ["stressed", "overwhelmed", "anxious", "burnt out", "burned out"]):
            flags["play_music"] = True
            return (
                "🧘 Let’s take a deep breath together. You’ve been doing your best — that’s enough. "
                "Want a 5-minute reset, a short walk reminder, or some calm music <span class='pulse'>🎵</span>?",
                flags,
            )

        if any(w in text for w in ["great", "good", "amazing", "happy", "excited"]):
            return (
                "✨ That’s awesome! Love the energy. Want me to line up a quick win for today, "
                "or plan something fun later?",
                flags,
            )

    return (None, {})



# --------------------
# Spotify Embed Helper (no API key; public playlist)
# --------------------
def spotify_embed_html(playlist_url: str):
    # Expect a normal playlist link like https://open.spotify.com/playlist/...
    # Convert to embeddable
    if "open.spotify.com" in playlist_url:
        src = playlist_url.replace("open.spotify.com/", "open.spotify.com/embed/")
        return f"""
        <iframe style="border-radius:12px" src="{src}" width="100%" height="352"
        frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
        """
    return ""

# A cheerful public playlist (feel free to swap this with your favorite)
UPLIFTING_PLAYLIST = "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"

# --------------------
# Pages
# --------------------
if nav == "Home":
    safe_logo("assets/ai_buddy_logo.png", width=200)
    st.markdown("## OrbyAI: Your AI Buddy that Orbits Around **You**!")
    st.write(
        "Empathetic conversations, wellness nudges, and smart scheduling, all in one friendly companion."
    )
    if st.button("💡 Generate Smart Day Plan"):
        st.success("✅ Your personalized day plan is ready:")
        st.write("• 09:00 - Prioritize key emails")
        st.write("• 12:30 - Mindful lunch break")
        st.write("• 15:00 - Focus block for creative work")
        st.write("• 18:00 - Connect with your friend 💬")
        st.balloons()


elif nav == "Chat":
    st.subheader("🗣️ Chat with OrbyAI")
    st.caption("Your AI Buddy Always Orbiting Around You!")

    # render conversation
    for role, msg in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(msg, unsafe_allow_html=True)

    # action surfaces from prior static reply
    if st.session_state.play_music:
        st.info("Uplifting music ready to play:")
        st.components.v1.html(spotify_embed_html(UPLIFTING_PLAYLIST), height=380)
    if st.session_state.connect_friend:
        with st.expander("💌 Connect with a friend (placeholder)"):
            st.text_input("Friend’s name (optional)", key="friend_name")
            st.text_area("Message draft", value="Hey — just checking in. Would love to catch up when you’re free 💙")
            st.button("Send (coming soon)", disabled=True)
            st.caption("This is a placeholder for future SMS/Email integrations.")

    # chat input
    prompt = st.chat_input("Say something to your AI Buddy...")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        # First try Smart Mood Replies
        reply, flags = get_static_reply(prompt, wellness_enabled=st.session_state.wellness_mode)

        if reply is None:
            # Fallback to a simple rule-based friendly response to avoid external API dependency
            reply = (
                "I’m here with you. Tell me more — is today feeling busy, calm, or somewhere in between? "
                "I can help set a tiny goal or suggest a short break."
            )
            flags = {}

        # Set action flags
        st.session_state.play_music = bool(flags.get("play_music"))
        st.session_state.connect_friend = bool(flags.get("connect_friend"))

        st.session_state.chat.append(("assistant", reply))
        st.rerun()

elif nav == "Calendar":

    # --- Dynamic date header ---
    today = datetime.now().strftime("%A, %B %d")
    st.markdown(f"### 📅 Today’s Plan - {today}")

    # --- Appointments section ---
    st.markdown("#### 🩺 Appointments")
    st.markdown(
        """
        - **10:00 AM** – 🧘 Therapy Session  
        - **2:00 PM** – 💬 Follow-up with Dr. Smith
        """
    )

    st.progress(60)  # progress bar to show "day progress"

    # --- Tasks section ---
    st.markdown("#### ✅ Tasks / Activities")

    # Initialize session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = [
            {"task": "Morning meditation", "done": True},
            {"task": "Go for a 30-minute walk", "done": False},
            {"task": "Prepare a healthy lunch", "done": False},
        ]

    # Display task checklist
    updated_tasks = []
    for t in st.session_state.tasks:
        done = st.checkbox(t["task"], value=t["done"])
        updated_tasks.append({"task": t["task"], "done": done})
    st.session_state.tasks = updated_tasks

    # Add new task
    new_task = st.text_input("Add a new task:")
    if st.button("➕ Add Task") and new_task.strip():
        st.session_state.tasks.append({"task": new_task.strip(), "done": False})
        st.rerun()

     #header for tip
    st.caption("💡 Tip: Balance productivity with rest — even small wins count.")

    # --- Calendar preview ---
    st.divider()
    st.markdown("#### 📆 Week Overview")

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Tasks": [3, 2, 4, 3, 2, 1, 0],
    })
    st.bar_chart(df.set_index("Day"), height=200, use_container_width=True)

   


elif nav == "Mail":
    st.subheader("📧 Mail Insights")

    df = seed_emails()

    # Color mapping
    def color_priority(val):
        color = ""
        if val.lower() == "high":
            color = "background-color: #ffcccc; color: #b30000; font-weight: 600;"  # red
        elif val.lower() == "low":
            color = "background-color: #e6ffed; color: #008000; font-weight: 500;"  # green
        elif val.lower() == "Medium":
            color = "background-color: #fff7cc; color: #b38f00; font-weight: 500;"  # yellow
        return color

    # Apply color styling
    styled_df = df.style.applymap(color_priority, subset=["Priority"])

    st.dataframe(styled_df, use_container_width=True)

    st.caption("Extracts action items and deadlines from emails.")


elif nav == "Deliverables":
    st.subheader("📝 Deliverable & Assignment Tracker")
    tasks = [
        {"Task": "Prepare presentation deck", "Due": "Tomorrow", "Status": "In Progress"},
        {"Task": "Coffe chat with Sherly", "Due": "Friday", "Status": "Not Started"},
        {"Task": "Book therapy session", "Due": "Today", "Status": "Open"},
    ]
    st.dataframe(pd.DataFrame(tasks), use_container_width=True)
    st.caption("Stay organized and balanced with proactive reminders.")

elif nav == "Approvals":
    st.subheader("Human Approval Workflow")
    st.write("Safety by design: route sensitive actions for approval.")
    st.text_area("Pending action :", "Send a check-in message to Alex.")
    if st.button("Approve"):
        st.success("Approved and queued.")

elif nav == "Support":
    st.subheader("🧘 Support & Wellness Resources")

    # --- Immediate Emergency ---
    st.markdown("### 🚨 Immediate Emergency")
    st.error("If you're in danger or need immediate help, please call emergency services.")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Jane Doe (Therapist)**  \n📞 111-222-3333")
    with col2:
        st.button("📞 Call 911 Emergency", use_container_width=True)
        st.button("💬 Call Jane Now", use_container_width=True)

    st.divider()

    # --- Resources & Tools ---
    st.markdown("### 📚 Resources & Tools")

    if st.button("💨 Breathing Exercises", use_container_width=True):
        st.video("https://www.youtube.com/watch?v=inpok4MKVLM")  # 5-Min Relaxing Breathing

    if st.button("📰 Read Helpful Articles", use_container_width=True):
        st.markdown(
            """
            - [How to Manage Stress (Mind.org)](https://www.mind.org.uk/information-support/types-of-mental-health-problems/stress/)
            - [Coping with Loneliness (CAMH)](https://www.camh.ca/)
            - [Daily Mental Health Tips](https://www.healthline.com/health/mental-health)
            """
        )

    if st.button("🧑‍⚕️ Find a Therapist Near You", use_container_width=True):
        st.markdown("[🔗 Open Google Maps](https://www.google.com/maps/search/therapist+near+me)")

else:
    st.subheader("⚙️ Settings")
    st.toggle("Demo Mode", value=True)
    st.text_input("Calendar Provider", "Google")
    st.text_input("AI Model (optional)", "Gemini / OpenAI")
    st.caption("Future-ready for enterprise integrations.")

st.divider()
# --- FOOTER CONTENT ---
st.markdown(
    """
    <div class="footer">
        © 2025 <strong>OrbyAI</strong> - Engineering empathy with intelligence. 
    </div>
    """,
    unsafe_allow_html=True
)
