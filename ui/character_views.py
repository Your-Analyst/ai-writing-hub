import streamlit as st

from db import add_character, get_characters
from ui.components import story_selector


def render_characters():
    story_id = story_selector()
    if not story_id:
        return

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add Character</div>', unsafe_allow_html=True)

    name = st.text_input("Name", key="character_name")
    role = st.text_input("Role", key="character_role")
    traits = st.text_input("Traits", placeholder="brave, observant, sharp-tongued", key="character_traits")
    goals = st.text_area("Goals", height=100, key="character_goals")
    description = st.text_area("Description", height=140, key="character_description")

    if st.button("Save Character 🌟", key="save_character_btn"):
        if not name.strip():
            st.error("Character name is required.")
        else:
            add_character(story_id, name, role, description, goals, traits)
            st.success("Character added.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    characters = get_characters(story_id)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Character Profiles</div>', unsafe_allow_html=True)

    if not characters:
        st.caption("No characters yet.")
    else:
        for character in characters:
            with st.expander(f"{character['name']} | {character['role'] or 'No role'}"):
                st.write(f"**Traits:** {character['traits'] or 'N/A'}")
                st.write(f"**Goals:** {character['goals'] or 'N/A'}")
                st.write(f"**Description:** {character['description'] or 'N/A'}")

    st.markdown("</div>", unsafe_allow_html=True)