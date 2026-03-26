import streamlit as st

from db import init_db
from ui.styles import inject_css
from ui.components import render_header, render_metrics
from ui.story_views import render_create_story, render_view_stories, render_export
from ui.character_views import render_characters
from ui.world_views import render_world_notes
from ui.ai_views import render_ai_tools


st.set_page_config(
    page_title="AI Writing Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
inject_css()

if "ai_output" not in st.session_state:
    st.session_state["ai_output"] = None

if "selected_chapter_id" not in st.session_state:
    st.session_state["selected_chapter_id"] = None

if "ai_mode" not in st.session_state:
    st.session_state["ai_mode"] = None


with st.sidebar:
    st.markdown("### Navigate")
    menu = st.radio(
        "",
        ["Create Story", "View Stories", "Characters", "World Notes", "AI Writing Tools", "Export"],
        label_visibility="collapsed",
    )

    st.markdown("")
    st.markdown("### 🌈 UI Mood")
    st.caption("Pale pink on the side. Blue sky and warm sunlight in the writing space.")

render_header()
render_metrics()
st.markdown("")

if menu == "Create Story":
    render_create_story()
elif menu == "View Stories":
    render_view_stories()
elif menu == "Characters":
    render_characters()
elif menu == "World Notes":
    render_world_notes()
elif menu == "AI Writing Tools":
    render_ai_tools()
elif menu == "Export":
    render_export()