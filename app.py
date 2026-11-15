"""Run with: python -m streamlit run app.py"""
import json
import os
from dataclasses import asdict
from dotenv import load_dotenv
import streamlit as st
from escape_room import v1, v2
from escape_room.engine import State, apply
from escape_room.llm import ModelUnavailable
from escape_room.world import INTRO

load_dotenv()
st.set_page_config(page_title="The Locked Library", page_icon="🗝️", layout="wide")
st.markdown("""<style>
.stApp {background: linear-gradient(135deg,#0d1520,#192b36);color:#ecede5;}
h1,h2,h3 {color:#ebcd91 !important;}
[data-testid="stSidebar"] {background:#101d28;}
[data-testid="stChatMessage"] {border:1px solid #334956;border-radius:12px;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🗝️ The Library")
    st.caption("AN AI ESCAPE ROOM")
    version = st.selectbox("Game version", ["Version 2 — Validated", "Version 1 — Baseline"])
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    model = os.getenv(provider.upper() + "_MODEL", "")
    online = st.toggle("Use online AI", value=False)
    st.caption(f"Provider: {provider.capitalize()} • Model: {model or 'not configured'}")
    st.caption("Uses local .env settings; use a free-tier project only." if online else
               "Offline practice • deterministic commands, no AI calls")
    if st.button("Restart game", use_container_width=True):
        for key in ["history", "game", "pending", "won"]:
            st.session_state.pop(key, None)
        st.rerun()

context = (version, online, provider, model)
if st.session_state.get("context") != context:
    for key in ["history", "game", "pending", "won"]:
        st.session_state.pop(key, None)
    st.session_state.context = context
if "history" not in st.session_state:
    st.session_state.history = [{"role": "assistant", "content": INTRO}]
    st.session_state.game = State()
    st.session_state.won = False

is_v2 = version.startswith("Version 2")
st.caption("THE LOCKED LIBRARY / A STUDY IN RELIABLE AI")
st.title("Every object holds a clue.")
st.write("Explore the room. Connect the clues. Find your way out.")
if is_v2:
    c1, c2, c3 = st.columns(3)
    c1.metric("Puzzles solved", f"{len(st.session_state.game.solved)} / 3")
    c2.metric("Items collected", len(st.session_state.game.inventory))
    c3.metric("Exit", "OPEN" if st.session_state.game.escaped else "LOCKED")
else:
    st.warning("V1 relies on the model for rules and memory. Its escape claims are not independently validated.")
if not online:
    st.info("Offline practice supports V2 only. Enable online AI to run the actual AI versions.")
if online and not (os.getenv(provider.upper() + "_API_KEY") and model):
    st.warning("API configuration is missing. Add your key and free-tier model to .env, then restart Streamlit.")

with st.sidebar:
    st.subheader("How to play")
    st.write("Type one action at a time. In V2, review it and press Confirm action.")
    st.code("examine bookshelf\ntake key\nuse key on desk\nenter 1234 on drawer\nanswer YOUR_ANSWER\nexamine painting\ninventory", language=None)
    if is_v2:
        st.subheader("Your inventory")
        st.write(", ".join(st.session_state.game.inventory) or "Empty")
    transcript = {"version": version, "mode": provider.capitalize() if online else "offline",
                  "provider": provider if online else None,
                  "model": model if online else None,
                  "messages": st.session_state.history,
                  "state": st.session_state.game.public() if is_v2 else None}
    st.download_button("Download session evidence", json.dumps(transcript, indent=2),
                       "escape-room-session.json", "application/json")

for row in st.session_state.history:
    with st.chat_message(row["role"]):
        st.write(row["content"])
won = st.session_state.game.escaped if is_v2 else st.session_state.won
if won:
    st.success("You escaped! Restart to explore again.")
if is_v2 and st.session_state.get("pending"):
    message, action = st.session_state.pending
    st.info("Review interpreted action before it reaches the rule engine.")
    st.json(asdict(action))
    confirm, cancel = st.columns(2)
    if confirm.button("Confirm action", type="primary", use_container_width=True):
        outcome = apply(st.session_state.game, action)
        st.session_state.game = outcome.state
        narrative = ""
        if online:
            try:
                narrative = v2.atmosphere() + "\n\n"
            except ModelUnavailable:
                narrative = "[AI atmosphere unavailable; validated result follows.]\n\n"
        st.session_state.history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": narrative + outcome.text}])
        st.session_state.pop("pending")
        st.rerun()
    if cancel.button("Cancel action", use_container_width=True):
        st.session_state.pop("pending")
        st.rerun()
disabled = won or bool(st.session_state.get("pending")) or (not is_v2 and not online)
if message := st.chat_input("What would you like to do?", max_chars=500, disabled=disabled):
    try:
        with st.spinner("Reading your action…"):
            if is_v2:
                action = v2.propose(message, online=online)
                if action.verb == "invalid":
                    st.session_state.history.extend([
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": "I could not identify one permitted action. "
                         "Try 'examine bookshelf' or 'help'. No game state changed."}])
                else:
                    st.session_state.pending = (message, action)
            else:
                answer = v1.respond(st.session_state.history, message)
                st.session_state.won = "[ESCAPED]" in answer
                st.session_state.history.extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": answer.replace("[ESCAPED]", "")}])
        st.rerun()
    except ModelUnavailable as error:
        st.error(str(error))
