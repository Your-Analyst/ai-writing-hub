import streamlit as st

from db import (
    create_story,
    get_story,
    create_chapter,
    get_chapters,
    add_tag,
    get_tags,
    get_characters,
    get_world_notes,
    delete_story,
)
from export_utils import export_story_to_docx, export_story_to_pdf
from ui.components import story_selector, render_tag_pills


def render_create_story():
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Create a New Story</div>', unsafe_allow_html=True)

    title = st.text_input("Story title", key="create_story_title")
    genre = st.text_input("Genre", key="create_story_genre")
    summary = st.text_area("Summary", height=180, key="create_story_summary")

    if st.button("Save Story ✨", key="save_story_btn"):
        if not title.strip():
            st.error("A title is required.")
        else:
            story_id = create_story(title, genre, summary)
            st.success(f"Story created successfully. ID: {story_id}")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_view_stories():
    story_id = story_selector()
    if not story_id:
        return

    story = get_story(story_id)
    tags = get_tags(story_id)
    chapters = get_chapters(story_id)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f'<div class="section-title">📖 {story["title"]}</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🗑️ Delete Story", key=f"delete_story_btn_{story_id}"):
            st.session_state["confirm_delete_story"] = story_id

    st.write(f"**Genre:** {story['genre'] or 'N/A'}")
    st.write(f"**Summary:** {story['summary'] or 'No summary yet.'}")

    if st.session_state.get("confirm_delete_story") == story_id:
        st.warning("Are you sure you want to delete this story? This cannot be undone.")

        confirm_col1, confirm_col2 = st.columns(2)

        with confirm_col1:
            if st.button("Yes, delete it", key=f"confirm_delete_btn_{story_id}"):
                delete_story(story_id)
                st.session_state["confirm_delete_story"] = None
                st.success("Story deleted.")
                st.rerun()

        with confirm_col2:
            if st.button("Cancel", key=f"cancel_delete_btn_{story_id}"):
                st.session_state["confirm_delete_story"] = None
                st.rerun()

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    st.write("**Tags**")
    render_tag_pills(tags)

    new_tag = st.text_input(
        "Add a tag",
        placeholder="fantasy, dark fantasy, slow burn, political intrigue",
        key="view_story_new_tag",
    )
    if st.button("Add Tag", key="add_tag_btn"):
        if new_tag.strip():
            add_tag(story_id, new_tag)
            st.success("Tag added.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add Chapter</div>', unsafe_allow_html=True)

    chapter_title = st.text_input("Chapter title", key="new_chapter_title")
    chapter_content = st.text_area("Chapter content", height=260, key="new_chapter_content")

    if st.button("Save Chapter 🖋️", key="save_chapter_btn"):
        if chapter_content.strip():
            create_chapter(story_id, chapter_title, chapter_content)
            st.success("Chapter saved.")
            st.rerun()
        else:
            st.error("Chapter content is required.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Chapters</div>', unsafe_allow_html=True)

    if not chapters:
        st.caption("No chapters yet.")
    else:
        for chapter in chapters:
            with st.expander(chapter["chapter_title"] or "Untitled Chapter", expanded=False):
                st.text_area(
                    "Chapter preview",
                    value=chapter["content"],
                    height=220,
                    disabled=True,
                    key=f"chapter_preview_{chapter['id']}",
                )
                st.caption(f"Updated: {chapter['updated_at']}")

    st.markdown("</div>", unsafe_allow_html=True)


def render_export():
    story_id = story_selector()
    if not story_id:
        return

    story = get_story(story_id)
    tags = get_tags(story_id)
    characters = get_characters(story_id)
    world_notes = get_world_notes(story_id)
    chapters = get_chapters(story_id)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Export Story</div>', unsafe_allow_html=True)
    st.caption("Bundle your story and its notes into a portable format.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export to DOCX 📄", key="export_docx_btn"):
            path = export_story_to_docx(story, tags, characters, world_notes, chapters)
            st.success(f"DOCX exported to: {path}")

    with col2:
        if st.button("Export to PDF 🧾", key="export_pdf_btn"):
            path = export_story_to_pdf(story, tags, characters, world_notes, chapters)
            st.success(f"PDF exported to: {path}")

    st.markdown("</div>", unsafe_allow_html=True)