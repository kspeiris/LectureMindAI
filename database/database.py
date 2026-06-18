import sqlite3
import os

DB_PATH     = os.path.join(os.path.dirname(__file__), 'lecturemind.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


# ─────────────────────────────────────────────
# Connection helpers
# ─────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    if not os.path.exists(SCHEMA_PATH):
        print(f"Warning: schema.sql not found at {SCHEMA_PATH}")
        return

    with get_connection() as conn:
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())

        # ── Migrations for existing databases ───────────────────────────
        _add_column_if_missing(conn, 'lectures', 'file_hash', 'TEXT DEFAULT NULL')
        _add_column_if_missing(conn, 'mcqs', 'difficulty', "TEXT DEFAULT 'medium'")
        _add_column_if_missing(conn, 'notes', 'generated_at', 'DATETIME DEFAULT NULL')
        conn.commit()


def _add_column_if_missing(conn, table: str, column: str, col_def: str):
    """Safely add a column to a table if it doesn't already exist."""
    try:
        existing = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
        if column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
    except Exception as e:
        print(f"[DB Migration] Could not add {column} to {table}: {e}")


# ─────────────────────────────────────────────
# Lectures
# ─────────────────────────────────────────────

def add_lecture(title: str, filename: str, pages: int, word_count: int, file_hash: str = None) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO lectures (title, filename, pages, word_count, file_hash) VALUES (?, ?, ?, ?, ?)',
            (title, filename, pages, word_count, file_hash)
        )
        conn.commit()
        return cursor.lastrowid


def get_all_lectures() -> list:
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM lectures ORDER BY upload_date DESC')
        return [dict(row) for row in cursor.fetchall()]


def get_lecture(lecture_id: int) -> dict | None:
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM lectures WHERE id = ?', (lecture_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_lecture_count() -> int:
    with get_connection() as conn:
        return conn.execute('SELECT COUNT(*) FROM lectures').fetchone()[0]


def delete_lecture(lecture_id: int):
    """Delete a lecture and all its associated data (cascade)."""
    with get_connection() as conn:
        conn.execute('DELETE FROM lectures WHERE id = ?', (lecture_id,))
        conn.commit()


def check_duplicate_file(file_hash: str) -> dict | None:
    """Return existing lecture dict if file_hash already exists, else None."""
    if not file_hash:
        return None
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM lectures WHERE file_hash = ? LIMIT 1', (file_hash,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


# ─────────────────────────────────────────────
# Notes
# ─────────────────────────────────────────────

def save_notes(lecture_id: int, summary: str, keywords: str):
    """Insert or replace notes for a lecture (upsert on lecture_id)."""
    with get_connection() as conn:
        conn.execute(
            '''INSERT INTO notes (lecture_id, summary, keywords)
               VALUES (?, ?, ?)
               ON CONFLICT(lecture_id) DO UPDATE SET
                   summary      = excluded.summary,
                   keywords     = excluded.keywords,
                   generated_at = CURRENT_TIMESTAMP''',
            (lecture_id, summary, keywords)
        )
        conn.commit()


def get_notes(lecture_id: int) -> dict | None:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM notes WHERE lecture_id = ? ORDER BY id DESC LIMIT 1', (lecture_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def get_notes_count() -> int:
    with get_connection() as conn:
        return conn.execute('SELECT COUNT(*) FROM notes').fetchone()[0]


# ─────────────────────────────────────────────
# Flashcards
# ─────────────────────────────────────────────

def save_flashcards(lecture_id: int, flashcards: list):
    """Delete existing flashcards for lecture and insert fresh ones."""
    with get_connection() as conn:
        conn.execute('DELETE FROM flashcards WHERE lecture_id = ?', (lecture_id,))
        for fc in flashcards:
            conn.execute(
                'INSERT INTO flashcards (lecture_id, question, answer) VALUES (?, ?, ?)',
                (lecture_id, fc['question'], fc['answer'])
            )
        conn.commit()


def get_flashcards(lecture_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM flashcards WHERE lecture_id = ?', (lecture_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_flashcards_count() -> int:
    with get_connection() as conn:
        return conn.execute('SELECT COUNT(*) FROM flashcards').fetchone()[0]


# ─────────────────────────────────────────────
# MCQs
# ─────────────────────────────────────────────

def save_mcqs(lecture_id: int, mcqs: list):
    """Delete existing MCQs for lecture and insert fresh ones."""
    with get_connection() as conn:
        conn.execute('DELETE FROM mcqs WHERE lecture_id = ?', (lecture_id,))
        for mcq in mcqs:
            opts = mcq.get('options', [])
            conn.execute(
                '''INSERT INTO mcqs (lecture_id, question, option_a, option_b, option_c, option_d, correct_answer)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    lecture_id,
                    mcq['question'],
                    opts[0] if len(opts) > 0 else '',
                    opts[1] if len(opts) > 1 else '',
                    opts[2] if len(opts) > 2 else '',
                    opts[3] if len(opts) > 3 else '',
                    mcq['correct'],
                )
            )
        conn.commit()


def get_mcqs(lecture_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM mcqs WHERE lecture_id = ?', (lecture_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_mcq_count() -> int:
    with get_connection() as conn:
        return conn.execute('SELECT COUNT(*) FROM mcqs').fetchone()[0]


# ─────────────────────────────────────────────
# Quiz Results
# ─────────────────────────────────────────────

def save_quiz_result(lecture_id: int, score: int, total_questions: int):
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO quiz_results (lecture_id, score, total_questions) VALUES (?, ?, ?)',
            (lecture_id, score, total_questions)
        )
        conn.commit()


def get_quiz_results(lecture_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM quiz_results WHERE lecture_id = ? ORDER BY taken_at DESC',
            (lecture_id,)
        )
        return [dict(row) for row in cursor.fetchall()]


def get_all_quiz_results() -> list:
    """Return all quiz results joined with lecture titles for the dashboard."""
    with get_connection() as conn:
        cursor = conn.execute(
            '''SELECT qr.*, l.title as lecture_title
               FROM quiz_results qr
               JOIN lectures l ON l.id = qr.lecture_id
               ORDER BY qr.taken_at DESC''',
        )
        return [dict(row) for row in cursor.fetchall()]


# Initialise on import
init_db()
