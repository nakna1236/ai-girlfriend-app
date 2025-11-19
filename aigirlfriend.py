import streamlit as st
import google.generativeai as genai
import base64

st.set_page_config(page_title="AI Girlfriend", layout="centered")

# -----------------------------------------------
# CONFIG
# -----------------------------------------------
genai.configure(api_key="AIzaSyBgmCWbxsZv2UoK6TvGS-6xqKcariYH4eM")
model = genai.GenerativeModel("gemini-2.0-flash")

# -----------------------------------------------
# SESSION STATE INIT
# -----------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gf_name" not in st.session_state:
    st.session_state.gf_name = "AI Girlfriend ❤️"

if "gf_mood" not in st.session_state:
    st.session_state.gf_mood = "happy"

# -----------------------------------------------
# LOCAL AVATARS
# -----------------------------------------------
avatars = {
    "happy": "happy.png",
    "sad": "sad.png",
    "angry": "angry.png",
    "lovely": "lovely.png",
    "jealous": "jelous.png",
    "cute": "cute.png"  # gif support works!
}

# Load image as base64
def load_image_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -----------------------------------------------
# HEADER UI WITH AVATAR
# -----------------------------------------------
avatar_path = avatars[st.session_state.gf_mood]
avatar_b64 = load_image_base64(avatar_path)

st.markdown(
    f"""
    <div style='text-align:center;'>
        <img src="data:image/png;base64,{avatar_b64}" width="160" style="border-radius:20px;"><br>
        <h2 style='margin-top:10px;'>{st.session_state.gf_name} • {st.session_state.gf_mood}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------
# SETTINGS PANEL
# -----------------------------------------------
with st.expander("💖 Girlfriend Settings"):
    st.session_state.gf_name = st.text_input("Girlfriend Name", st.session_state.gf_name)

    st.session_state.gf_mood = st.selectbox(
        "Select Mood",
        ["happy", "sad", "angry", "lovely", "cute", "jealous"],
        index=["happy", "sad", "angry", "lovely", "cute", "jealous"].index(st.session_state.gf_mood)
    )
    st.write("Mood changes the avatar + tone of reply.")

# -----------------------------------------------
# CHAT DISPLAY
# -----------------------------------------------
st.markdown("### 💬 Chat")

chat_box = st.container()

with chat_box:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style='text-align:right; margin:8px;'>
                    <div style='display:inline-block; background:#DCF8C6; padding:10px 15px;
                    border-radius:12px; max-width:70%; color:black;'>{msg['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align:left; margin:8px;'>
                    <div style='display:inline-block; background:white; padding:10px 15px;
                    border-radius:12px; max-width:70%;
                    border:1px solid #eee;'>{msg['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------------------
# USER INPUT
# -----------------------------------------------
user_input = st.text_input("Type a message...")
send = st.button("Send")

# -----------------------------------------------
# SEND LOGIC
# -----------------------------------------------
if send and user_input.strip() != "":
    st.session_state.messages.append({"role": "user", "content": user_input})

    history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    prompt = f"""
    You are {st.session_state.gf_name}, the user's AI Girlfriend.
    Mood: {st.session_state.gf_mood}
    Tone: cute, emotional, girlfriend-like.

    Chat History:
    {history}

    Reply to the user's last message as a loving girlfriend.
    """

    reply = model.generate_content(prompt).text

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
