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


def get_history_parsed():
    """
    Return history rows with skill JSON parsed into
    real lists so templates can render skill chips.
    """

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    analyses = []

    for row in rows:

        analysis = dict(row)

        try:
            analysis["matching_skills"] = json.loads(
                analysis["matching_skills"] or "[]"
            )
        except (ValueError, TypeError):
            analysis["matching_skills"] = []

        try:
            analysis["missing_skills"] = json.loads(
                analysis["missing_skills"] or "[]"
            )
        except (ValueError, TypeError):
            analysis["missing_skills"] = []

        analyses.append(analysis)

    return analyses


def delete_history():
    """
    Remove all rows from the analyses table.
    """

    conn = get_connection()

    conn.execute("DELETE FROM analyses")

    conn.commit()
    conn.close()