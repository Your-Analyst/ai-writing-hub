import streamlit as st

from db import add_world_note, get_world_notes
from ui.components import story_selector


def render_world_notes():
    story_id = story_selector()
    if not story_id:
        return

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add World Note</div>', unsafe_allow_html=True)

    title = st.text_input("Note title", key="world_note_title")
    category = st.selectbox(
        "Category",
        ["General", "Location", "Magic System", "Faction", "History", "Religion", "Politics", "Technology"],
        key="world_note_category",
    )
    content = st.text_area("Content", height=180, key="world_note_content")

    if st.button("Save World Note 🗺️", key="save_world_note_btn"):
        if not title.strip() or not content.strip():
            st.error("Title and content are required.")
        else:
            add_world_note(story_id, title, category, content)
            st.success("World note added.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    notes = get_world_notes(story_id)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Lore Shelf</div>', unsafe_allow_html=True)

    if not notes:
        st.caption("No world notes yet.")
    else:
        for note in notes:
            with st.expander(f"{note['title']} [{note['category'] or 'General'}]"):
                st.write(note["content"])

    st.markdown("</div>", unsafe_allow_html=True)