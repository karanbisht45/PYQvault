import sqlite3
import os
import hashlib
from typing import Optional, Dict, Any, List

BASE_DIR = os.path.dirname(__file__)
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_FILE = os.path.join(DB_FOLDER, "pyq_db.sqlite")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

SALT = "pyq_salt_2025"

def _get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('uploader','viewer'))
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS pyqs (
                    pyq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    subject TEXT,
                    semester TEXT,
                    year TEXT,
                    course_code TEXT,
                    university TEXT,
                    tags TEXT,
                    file_path TEXT,
                    ocr_text TEXT,
                    uploaded_by INTEGER,
                    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(uploaded_by) REFERENCES users(user_id)
                )""")
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    to_hash = (password + SALT).encode("utf-8")
    return hashlib.sha256(to_hash).hexdigest()

def add_user(username: str, email: str, password: str, role: str = "viewer") -> bool:
    conn = _get_conn()
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                  (username, email, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = get_user_by_email(email)
    if not user:
        return None
    if user["password"] == hash_password(password):
        return user
    return None

def add_pyq(metadata: Dict[str, Any]) -> int:
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""INSERT INTO pyqs
                 (title, subject, semester, year, course_code, university, tags, file_path, ocr_text, uploaded_by)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (metadata.get("title"), metadata.get("subject"), metadata.get("semester"),
               metadata.get("year"), metadata.get("course_code"), metadata.get("university"),
               metadata.get("tags"), metadata.get("file_path"), metadata.get("ocr_text"),
               metadata.get("uploaded_by")))
    conn.commit()
    pyq_id = c.lastrowid
    conn.close()
    return pyq_id

def _build_query(filters: Dict[str, Any]):
    query = "SELECT * FROM pyqs"
    params: List[Any] = []
    if not filters:
        return query + " ORDER BY upload_date DESC", params
    clauses = []
    for k, v in filters.items():
        if v:
            clauses.append(f"{k} LIKE ?")
            params.append(f"%{v}%")
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY upload_date DESC"
    return query, params

def get_pyqs(filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    conn = _get_conn()
    c = conn.cursor()
    query, params = _build_query(filters or {})
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_pyq(pyq_id: int, user_id: int):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM pyqs WHERE pyq_id=? AND uploaded_by=?", (pyq_id, user_id))
    conn.commit()
    conn.close()
    return True, "Deleted"
