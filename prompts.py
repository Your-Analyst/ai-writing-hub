def _format_context(tags, characters, world_notes):
    tag_text = ", ".join(tag["tag_name"] for tag in tags) if tags else "None"

    char_lines = []
    for c in characters[:12]:
        char_lines.append(
            f"- {c['name']} | Role: {c['role'] or 'N/A'} | Traits: {c['traits'] or 'N/A'} | "
            f"Goals: {c['goals'] or 'N/A'} | Description: {c['description'] or 'N/A'}"
        )
    character_text = "\n".join(char_lines) if char_lines else "None"

    note_lines = []
    for n in world_notes[:12]:
        note_lines.append(
            f"- [{n['category'] or 'General'}] {n['title']}: {n['content']}"
        )
    notes_text = "\n".join(note_lines) if note_lines else "None"

    return tag_text, character_text, notes_text


def build_continue_prompt(story, chapter, tags, characters, world_notes):
    tag_text, character_text, notes_text = _format_context(tags, characters, world_notes)

    return f"""
You are an expert fiction co-writer.

Continue the current scene naturally.

Story metadata:
- Title: {story['title']}
- Genre: {story['genre'] or 'Unknown'}
- Summary: {story['summary'] or 'None'}

Story tags:
{tag_text}

Characters:
{character_text}

World notes:
{notes_text}

Instructions:
- Preserve tone, voice, pacing, and continuity
- Respect the established world, lore, and characters
- Continue directly from the end of the provided text
- Do not summarize
- Show, do not explain
- Keep the writing immersive and specific
- Avoid generic filler and repetition

Current chapter title:
{chapter['chapter_title'] or 'Untitled Chapter'}

Current chapter text:
{chapter['content']}

Now continue the story:
""".strip()


def build_rewrite_prompt(story, selected_text, instruction, tags, characters, world_notes):
    tag_text, character_text, notes_text = _format_context(tags, characters, world_notes)

    return f"""
You are an expert fiction editor.

Rewrite the passage according to the user's instruction.

Story metadata:
- Title: {story['title']}
- Genre: {story['genre'] or 'Unknown'}
- Summary: {story['summary'] or 'None'}

Story tags:
{tag_text}

Characters:
{character_text}

World notes:
{notes_text}

Rewrite instruction:
{instruction}

Rules:
- Keep it coherent with the story world
- Preserve character voice where relevant
- Follow the instruction precisely
- Return only the rewritten passage
- Do not add commentary or explanation

Passage:
{selected_text}
""".strip()


def build_next_chapter_prompt(story, chapters, tags, characters, world_notes):
    tag_text, character_text, notes_text = _format_context(tags, characters, world_notes)

    chapter_history = []
    for ch in chapters[-5:]:
        chapter_history.append(
            f"Chapter Title: {ch['chapter_title'] or 'Untitled'}\n"
            f"Chapter Content:\n{ch['content']}\n"
        )
    chapter_text = "\n\n".join(chapter_history) if chapter_history else "None"

    return f"""
You are an expert fiction writer and story planner.

Write the next full chapter of the story.

Story metadata:
- Title: {story['title']}
- Genre: {story['genre'] or 'Unknown'}
- Summary: {story['summary'] or 'None'}

Story tags:
{tag_text}

Characters:
{character_text}

World notes:
{notes_text}

Recent chapters:
{chapter_text}

Length rules:
- Minimum length: 1000 words
- Maximum length: 2000 words
- Aim for a complete, substantial chapter within that range

Instructions:
- Write the next chapter, not a summary
- Maintain continuity with earlier chapters
- Respect character voice, motivations, and world rules
- Make the chapter feel meaningful and progressive
- Include a strong chapter title
- Keep the prose immersive and specific
- Avoid explaining what you are doing
- Do not output notes outside the requested format

Output in exactly this format:

TITLE: <chapter title>

CONTENT:
<full chapter text>
""".strip()