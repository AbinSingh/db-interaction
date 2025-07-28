from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()
DB_PATH = "qa_feedback.db"

class CommentUpdate(BaseModel):
    comment: str

class QAItem(BaseModel):
    id: int
    question: str
    prediction: str
    ground_truth: str
    comment: str | None = None

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/questions", response_model=list[QAItem])
def get_questions():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM qa_feedback LIMIT 10").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/comment/{qa_id}")
def update_comment(qa_id: int, update: CommentUpdate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE qa_feedback SET comment = ? WHERE id = ?", (update.comment, qa_id))
    conn.commit()
    conn.close()
    return {"message": "Comment updated"}
