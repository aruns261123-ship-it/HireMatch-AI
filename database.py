import sqlite3
import json
from datetime import datetime

DATABASE = "hirematch.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            match_score REAL NOT NULL,
            similarity_score REAL NOT NULL,
            skill_score REAL NOT NULL,
            matching_skills TEXT,
            missing_skills TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(filename, result):
    conn = get_connection()

    conn.execute("""
        INSERT INTO analyses (
            filename,
            match_score,
            similarity_score,
            skill_score,
            matching_skills,
            missing_skills,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        result["match_score"],
        result["similarity_score"],
        result["skill_score"],
        json.dumps(result["matching_skills"]),
        json.dumps(result["missing_skills"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]