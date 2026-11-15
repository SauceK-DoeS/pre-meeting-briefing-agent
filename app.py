"""
Pre-Meeting Briefing Agent
Maintained by Praveen (@SauceK-DoeS) & Kenneth Ansel
"""

import re
from datetime import time as dtime

import streamlit as st

from src import config
from src.briefing import generate_briefing

st.set_page_config(page_title="Pre-Meeting Briefing Agent", page_icon="📋")
st.title("📋 Pre-Meeting Briefing Agent")
st.caption("A source-backed, one-page briefing from the last 30 days of news.")

problems = config.check_config()
if problems:
    st.error("Setup incomplete:\n\n" + "\n".join(f"- {p}" for p in problems))
    st.stop()

with st.form("briefing_form"):
    subject = st.text_input("Company or person", placeholder="e.g. Nebius")
    c1, c2 = st.columns(2)
    meeting_date = c1.date_input("Meeting date")
    meeting_time = c2.time_input("Meeting time", value=dtime(10, 0))
    meeting_type = st.selectbox(
        "Meeting type",
        ["Sales call", "Partnership", "Investor meeting", "Business development", "General"],
    )
    submitted = st.form_submit_button("Generate briefing", type="primary")

if submitted:
    if not subject.strip():
        st.warning("Enter a company or person.")
    else:
        with st.spinner("Researching the last 30 days..."):
            try:
                st.session_state["briefing"] = generate_briefing(
                    subject.strip(), f"{meeting_date} {meeting_time:%H:%M}", meeting_type
                )
                st.session_state["subject"] = subject.strip()
            except Exception as e:
                st.session_state.pop("briefing", None)
                st.error(f"Could not generate the briefing: {e}")

# Stored in session_state so it stays visible after clicking Download
if "briefing" in st.session_state:
    st.markdown(st.session_state["briefing"])
    safe = re.sub(r"[^a-zA-Z0-9]+", "-", st.session_state["subject"]).strip("-").lower()
    st.download_button(
        "Download .md",
        st.session_state["briefing"],
        file_name=f"briefing-{safe}.md",
        mime="text/markdown",
    )