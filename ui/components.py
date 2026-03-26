import streamlit as st

from db import get_stories, get_chapters, get_characters


def render_header():
    st.markdown(
        '<div class="main-title">📚 AI Writing Hub</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-title">A bright little studio for stories, characters, lore, and AI-assisted drafting.</div>',
        unsafe_allow_html=True,
    )


def render_metrics():
    stories = get_stories()
    story_count = len(stories)
    chapter_count = sum(len(get_chapters(s["id"])) for s in stories) if stories else 0
    character_count = sum(len(get_characters(s["id"])) for s in stories) if stories else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="metric-number">{story_count}</div>
                <div class="metric-label">Stories</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="metric-number">{chapter_count}</div>
                <div class="metric-label">Chapters</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="mini-card">
                <div class="metric-number">{character_count}</div>
                <div class="metric-label">Characters</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def story_selector(label="Choose a story"):
    stories = get_stories()
    if not stories:
        st.info("No stories yet. Create one first.")
        return None

    story_map = {f"{s['title']} (ID {s['id']})": s["id"] for s in stories}
    selected_label = st.selectbox(label, list(story_map.keys()))
    return story_map[selected_label]


def render_tag_pills(tags):
    if not tags:
        st.caption("No tags yet.")
        return

    pills_html = "".join([f'<span class="pill">{tag["tag_name"]}</span>' for tag in tags])
    st.markdown(pills_html, unsafe_allow_html=True)