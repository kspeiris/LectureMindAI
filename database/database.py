import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'lecturemind.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(SCHEMA_PATH):
        print(f"Warning: schema.sql not found at {SCHEMA_PATH}")
        return
        
    with get_connection() as conn:
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()

# --- Lectures ---

def add_lecture(title, filename, pages, word_count):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO lectures (title, filename, pages, word_count)
            VALUES (?, ?, ?, ?)
        ''', (title, filename, pages, word_count))
        conn.commit()
        return cursor.lastrowid

def get_all_lectures():
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM lectures ORDER BY upload_date DESC')
        return [dict(row) for row in cursor.fetchall()]

def get_lecture(lecture_id):
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM lectures WHERE id = ?', (lecture_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_lecture_count():
    with get_connection() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM lectures')
        return cursor.fetchone()[0]

# --- Notes ---

def save_notes(lecture_id, summary, keywords):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notes (lecture_id, summary, keywords)
            VALUES (?, ?, ?)
        ''', (lecture_id, summary, keywords))
        conn.commit()
        return cursor.lastrowid

def get_notes(lecture_id):
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM notes WHERE lecture_id = ? ORDER BY id DESC LIMIT 1', (lecture_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# --- Flashcards ---

def save_flashcards(lecture_id, flashcards):
    """flashcards is a list of dicts: [{'question': '...', 'answer': '...'}, ...]"""
    with get_connection() as conn:
        cursor = conn.cursor()
        for fc in flashcards:
            cursor.execute('''
                INSERT INTO flashcards (lecture_id, question, answer)
                VALUES (?, ?, ?)
            ''', (lecture_id, fc['question'], fc['answer']))
        conn.commit()

def get_flashcards(lecture_id):
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM flashcards WHERE lecture_id = ?', (lecture_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_flashcards_count():
    with get_connection() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM flashcards')
        return cursor.fetchone()[0]

# --- MCQs ---

def save_mcqs(lecture_id, mcqs):
    """mcqs is a list of dicts: [{'question': '...', 'options': ['A', 'B', 'C', 'D'], 'correct': '...'}]"""
    with get_connection() as conn:
        cursor = conn.cursor()
        for mcq in mcqs:
            cursor.execute('''
                INSERT INTO mcqs (lecture_id, question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                lecture_id, 
                mcq['question'], 
                mcq['options'][0] if len(mcq['options']) > 0 else '',
                mcq['options'][1] if len(mcq['options']) > 1 else '',
                mcq['options'][2] if len(mcq['options']) > 2 else '',
                mcq['options'][3] if len(mcq['options']) > 3 else '',
                mcq['correct']
            ))
        conn.commit()

def get_mcqs(lecture_id):
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM mcqs WHERE lecture_id = ?', (lecture_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_mcq_count():
    with get_connection() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM mcqs')
        return cursor.fetchone()[0]

# --- Quiz Results ---

def save_quiz_result(lecture_id, score, total_questions):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_results (lecture_id, score, total_questions)
            VALUES (?, ?, ?)
        ''', (lecture_id, score, total_questions))
        conn.commit()

def get_quiz_results(lecture_id):
    with get_connection() as conn:
        cursor = conn.execute('SELECT * FROM quiz_results WHERE lecture_id = ? ORDER BY taken_at DESC', (lecture_id,))
        return [dict(row) for row in cursor.fetchall()]

# Initialize the database on import
init_db()
