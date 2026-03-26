import sqlite3
from contextlib import closing
from datetime import datetime

DB_PATH = "stories.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def now_str():
    return datetime.utcnow().isoformat(timespec="seconds")


def init_db():
    with closing(get_connection()) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT,
                summary TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                chapter_title TEXT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS story_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                tag_name TEXT NOT NULL,
                UNIQUE(story_id, tag_name),
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                role TEXT,
                description TEXT,
                goals TEXT,
                traits TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS world_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chapter_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_id INTEGER NOT NULL,
                version_label TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
            )
        """)


# ----------------------------
# Stories
# ----------------------------

def create_story(title: str, genre: str, summary: str) -> int:
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("""
            INSERT INTO stories (title, genre, summary, created_at)
            VALUES (?, ?, ?, ?)
        """, (title.strip(), genre.strip(), summary.strip(), now_str()))
        return cur.lastrowid


def get_stories():
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM stories
            ORDER BY id DESC
        """)
        return cur.fetchall()


def get_story(story_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
        return cur.fetchone()


def delete_story(story_id: int):
    with closing(get_connection()) as conn, conn:
        chapter_ids = conn.execute(
            "SELECT id FROM chapters WHERE story_id = ?",
            (story_id,)
        ).fetchall()

        for row in chapter_ids:
            conn.execute("DELETE FROM chapter_versions WHERE chapter_id = ?", (row["id"],))

        conn.execute("DELETE FROM chapters WHERE story_id = ?", (story_id,))
        conn.execute("DELETE FROM story_tags WHERE story_id = ?", (story_id,))
        conn.execute("DELETE FROM characters WHERE story_id = ?", (story_id,))
        conn.execute("DELETE FROM world_notes WHERE story_id = ?", (story_id,))
        conn.execute("DELETE FROM stories WHERE id = ?", (story_id,))


# ----------------------------
# Chapters
# ----------------------------

def create_chapter(story_id: int, chapter_title: str, content: str) -> int:
    timestamp = now_str()
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("""
            INSERT INTO chapters (story_id, chapter_title, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (story_id, chapter_title.strip(), content.strip(), timestamp, timestamp))
        return cur.lastrowid


def get_chapters(story_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM chapters
            WHERE story_id = ?
            ORDER BY id ASC
        """, (story_id,))
        return cur.fetchall()


def get_chapter(chapter_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
        return cur.fetchone()


def update_chapter_content(chapter_id: int, content: str):
    with closing(get_connection()) as conn, conn:
        conn.execute("""
            UPDATE chapters
            SET content = ?, updated_at = ?
            WHERE id = ?
        """, (content.strip(), now_str(), chapter_id))


def append_to_chapter(chapter_id: int, additional_text: str):
    chapter = get_chapter(chapter_id)
    if not chapter:
        return

    current = chapter["content"] or ""
    updated = f"{current.rstrip()}\n\n{additional_text.strip()}"
    update_chapter_content(chapter_id, updated)


# ----------------------------
# Tags
# ----------------------------

def add_tag(story_id: int, tag_name: str):
    clean_tag = tag_name.strip().lower()
    if not clean_tag:
        return

    with closing(get_connection()) as conn, conn:
        conn.execute("""
            INSERT OR IGNORE INTO story_tags (story_id, tag_name)
            VALUES (?, ?)
        """, (story_id, clean_tag))


def get_tags(story_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM story_tags
            WHERE story_id = ?
            ORDER BY tag_name ASC
        """, (story_id,))
        return cur.fetchall()


# ----------------------------
# Characters
# ----------------------------

def add_character(story_id: int, name: str, role: str, description: str, goals: str, traits: str) -> int:
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("""
            INSERT INTO characters (story_id, name, role, description, goals, traits, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            story_id,
            name.strip(),
            role.strip(),
            description.strip(),
            goals.strip(),
            traits.strip(),
            now_str()
        ))
        return cur.lastrowid


def get_characters(story_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM characters
            WHERE story_id = ?
            ORDER BY name COLLATE NOCASE ASC
        """, (story_id,))
        return cur.fetchall()


# ----------------------------
# World Notes
# ----------------------------

def add_world_note(story_id: int, title: str, category: str, content: str) -> int:
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("""
            INSERT INTO world_notes (story_id, title, category, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            story_id,
            title.strip(),
            category.strip(),
            content.strip(),
            now_str()
        ))
        return cur.lastrowid


def get_world_notes(story_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM world_notes
            WHERE story_id = ?
            ORDER BY category ASC, title COLLATE NOCASE ASC
        """, (story_id,))
        return cur.fetchall()


# ----------------------------
# Chapter Versions
# ----------------------------

def save_chapter_version(chapter_id: int, version_label: str, content: str):
    with closing(get_connection()) as conn, conn:
        conn.execute("""
            INSERT INTO chapter_versions (chapter_id, version_label, content, created_at)
            VALUES (?, ?, ?, ?)
        """, (chapter_id, version_label.strip(), content, now_str()))


def get_chapter_versions(chapter_id: int):
    with closing(get_connection()) as conn:
        cur = conn.execute("""
            SELECT * FROM chapter_versions
            WHERE chapter_id = ?
            ORDER BY id DESC
        """, (chapter_id,))
        return cur.fetchall()