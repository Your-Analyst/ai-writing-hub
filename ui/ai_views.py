import streamlit as st

from db import (
    get_story,
    get_tags,
    get_characters,
    get_world_notes,
    get_chapters,
    get_chapter,
    create_chapter,
    append_to_chapter,
    update_chapter_content,
    save_chapter_version,
    get_chapter_versions,
)
from llm import generate_text, OLLAMA_MODEL
from prompts import (
    build_continue_prompt,
    build_rewrite_prompt,
    build_next_chapter_prompt,
)
from ui.components import story_selector


def parse_generated_chapter(raw_text: str):
    raw_text = raw_text.strip()

    if "CONTENT:" in raw_text and "TITLE:" in raw_text:
        title_part = raw_text.split("CONTENT:", 1)[0]
        content_part = raw_text.split("CONTENT:", 1)[1]

        title = title_part.replace("TITLE:", "").strip()
        content = content_part.strip()

        if title and content:
            return title, content

    return "Untitled Chapter", raw_text


def render_word_count_badge(text: str):
    word_count = len(text.split()) if text else 0
    badge_color = "#5c4c73"

    if word_count < 1000:
        status = "Below target"
        badge_bg = "#ffe3ec"
        badge_border = "#f3b8cc"
    elif word_count > 2000:
        status = "Above target"
        badge_bg = "#fff0d6"
        badge_border = "#f1d18a"
    else:
        status = "Within target"
        badge_bg = "#e8f8ef"
        badge_border = "#b8e3c6"

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            margin: 0.4rem 0 0.8rem 0;
            padding: 0.5rem 0.9rem;
            border-radius: 999px;
            background: {badge_bg};
            border: 1px solid {badge_border};
            color: {badge_color};
            font-weight: 700;
            font-size: 0.95rem;
        ">
            📊 Word Count: {word_count} · {status}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_tools():
    story_id = story_selector()
    if not story_id:
        return

    story = get_story(story_id)
    tags = get_tags(story_id)
    characters = get_characters(story_id)
    world_notes = get_world_notes(story_id)
    chapters = get_chapters(story_id)

    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Writing Tools</div>', unsafe_allow_html=True)
    st.caption(f"Connected model: {OLLAMA_MODEL}")

    if not chapters:
        st.info("Add a chapter first.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    chapter_map = {f"{c['chapter_title'] or 'Untitled'} (ID {c['id']})": c["id"] for c in chapters}
    selected_chapter_label = st.selectbox(
        "Choose chapter",
        list(chapter_map.keys()),
        key="ai_selected_chapter",
    )
    chapter_id = chapter_map[selected_chapter_label]
    chapter = get_chapter(chapter_id)

    tool = st.segmented_control(
        "Choose tool",
        ["Continue Scene", "Rewrite Passage", "Generate Next Chapter"],
        key="ai_tool_mode",
    )

    if tool == "Continue Scene":
        st.text_area(
            "Current chapter text",
            value=chapter["content"],
            height=250,
            key=f"continue_preview_{chapter_id}",
        )

        if st.button("Generate Continuation ✨", key="generate_continuation_btn"):
            prompt = build_continue_prompt(story, chapter, tags, characters, world_notes)
            with st.spinner("Summoning prose from the local model..."):
                output = generate_text(prompt)

            st.session_state["ai_output"] = output
            st.session_state["selected_chapter_id"] = chapter_id
            st.session_state["ai_mode"] = "continue"
            st.rerun()

    elif tool == "Rewrite Passage":
        selected_text = st.text_area(
            "Passage to rewrite",
            height=180,
            key="rewrite_selected_text",
        )
        instruction = st.text_input(
            "Rewrite instruction",
            placeholder="Make it more atmospheric and tense",
            key="rewrite_instruction",
        )

        if st.button("Rewrite Passage 🎨", key="rewrite_passage_btn"):
            if not selected_text.strip() or not instruction.strip():
                st.error("Both the passage and instruction are required.")
            else:
                prompt = build_rewrite_prompt(
                    story=story,
                    selected_text=selected_text,
                    instruction=instruction,
                    tags=tags,
                    characters=characters,
                    world_notes=world_notes,
                )
                with st.spinner("Polishing the prose gears..."):
                    output = generate_text(prompt)

                st.session_state["ai_output"] = output
                st.session_state["selected_chapter_id"] = chapter_id
                st.session_state["ai_mode"] = "rewrite"
                st.rerun()

    elif tool == "Generate Next Chapter":
        st.caption("This will generate a brand new chapter based on the story so far.")

        if st.button("Generate Next Chapter 📘", key="generate_next_chapter_btn"):
            prompt = build_next_chapter_prompt(story, chapters, tags, characters, world_notes)
            with st.spinner("Drafting the next chapter..."):
                output = generate_text(prompt)

            st.session_state["ai_output"] = output
            st.session_state["selected_chapter_id"] = chapter_id
            st.session_state["ai_mode"] = "next_chapter"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("ai_output") and st.session_state.get("selected_chapter_id") == chapter_id:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Output</div>', unsafe_allow_html=True)

        ai_mode = st.session_state.get("ai_mode")
        selected_chapter = get_chapter(chapter_id)

        if ai_mode == "next_chapter":
            generated_title, generated_content = parse_generated_chapter(st.session_state["ai_output"])

            st.text_input(
                "Generated chapter title",
                value=generated_title,
                disabled=True,
                key="generated_chapter_title_preview",
            )

            render_word_count_badge(generated_content)

            st.text_area(
                "Generated chapter content",
                value=generated_content,
                height=360,
                key="next_chapter_preview",
            )

            if st.button("Save as New Chapter 📚", key="save_new_generated_chapter_btn"):
                create_chapter(story_id, generated_title, generated_content)
                st.success(f"New chapter saved: {generated_title}")
                st.session_state["ai_output"] = None
                st.session_state["ai_mode"] = None
                st.session_state["selected_chapter_id"] = None
                st.rerun()

        else:
            st.text_area(
                "Generated text",
                value=st.session_state["ai_output"],
                height=320,
                key="ai_output_preview",
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Append to Chapter", key="append_ai_output_btn"):
                    save_chapter_version(chapter_id, "Before AI Append", selected_chapter["content"])
                    append_to_chapter(chapter_id, st.session_state["ai_output"])
                    st.success("AI output appended to chapter.")
                    st.rerun()

            with col2:
                if st.button("Replace Chapter", key="replace_ai_output_btn"):
                    save_chapter_version(chapter_id, "Before AI Replace", selected_chapter["content"])
                    update_chapter_content(chapter_id, st.session_state["ai_output"])
                    st.success("Chapter replaced. Previous version saved.")
                    st.rerun()

            with col3:
                if st.button("Save as Version", key="save_ai_version_btn"):
                    save_chapter_version(chapter_id, "AI Draft Snapshot", st.session_state["ai_output"])
                    st.success("AI draft saved as a version snapshot.")

        versions = get_chapter_versions(chapter_id)

        st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Version History</div>', unsafe_allow_html=True)

        if not versions:
            st.caption("No saved versions yet.")
        else:
            for version in versions:
                with st.expander(f"{version['version_label']} | {version['created_at']}"):
                    st.text_area(
                        "Saved version",
                        value=version["content"],
                        height=180,
                        disabled=True,
                        key=f"version_preview_{version['id']}",
                    )

        st.markdown("</div>", unsafe_allow_html=True)