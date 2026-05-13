"""
Database Module for PixelAlchemy.
Handles all SQLite operations for saving artworks, patterns, and tracking lesson progress.
"""
import sqlite3
import logging
from pathlib import Path

DB_FILE = "pixelalchemy.db"

# Initialize logging for the app
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initializes the database tables if they do not exist."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Artworks table (Canvas Art and Patterns)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artworks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    type TEXT NOT NULL,  -- 'canvas', 'pattern', 'filter'
                    metadata TEXT
                )
            ''')
            
            # Lessons progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lessons_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_name TEXT UNIQUE NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            
            # Quiz scores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_name TEXT UNIQUE NOT NULL,
                    score INTEGER NOT NULL
                )
            ''')
            
            conn.commit()
            logging.info("Database initialized successfully.")
    except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
        logging.error(f"Database initialization failed: {e}")

def save_artwork(title, image_path, item_type, metadata=""):
    """Saves an artwork entry to the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO artworks (title, image_path, type, metadata) VALUES (?, ?, ?, ?)",
                (title, image_path, item_type, metadata)
            )
            conn.commit()
            logging.info(f"Saved artwork: {title}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Failed to save artwork {title}: {e}")
        return False

def get_all_artworks():
    """Fetches all artworks."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, image_path, type, metadata FROM artworks ORDER BY id DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch artworks: {e}")
        return []

def delete_artwork(artwork_id):
    """Deletes an artwork by ID."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM artworks WHERE id = ?", (artwork_id,))
            conn.commit()
            logging.info(f"Deleted artwork with ID {artwork_id}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Failed to delete artwork {artwork_id}: {e}")
        return False

def save_quiz_score(quiz_name, score):
    """Saves or updates a quiz score."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO quiz_scores (quiz_name, score) VALUES (?, ?) "
                "ON CONFLICT(quiz_name) DO UPDATE SET score = excluded.score",
                (quiz_name, score)
            )
            conn.commit()
            logging.info(f"Saved quiz score for {quiz_name}: {score}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Failed to save quiz score {quiz_name}: {e}")
        return False

def get_quiz_score(quiz_name):
    """Gets a quiz score."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT score FROM quiz_scores WHERE quiz_name = ?", (quiz_name,))
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error as e:
        logging.error(f"Failed to get quiz score {quiz_name}: {e}")
        return None
