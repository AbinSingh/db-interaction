from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from queue import Queue
from get_database import get_db_connection
from asyncio import Future

class QuestionRequest(BaseModel):
    account: str
    questions: List[str]

class CommentUpdate(BaseModel):
    comment: str

class QAItem(BaseModel):
    id: int
    question: str
    prediction: str
    ground_truth: str
    comment: str | None = None

request_queue = Queue()

router = APIRouter()

@router.get("/questions", response_model=list[QAItem])
def get_questions():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM qa_feedback LIMIT 10").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/comment/{qa_id}")
def update_comment(qa_id: int, update: CommentUpdate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE qa_feedback SET comment = ? WHERE id = ?", (update.comment, qa_id))
    conn.commit()
    conn.close()
    return {"message": "Comment updated"}

@router.post("/submit-questions")
async def submit_questions(req: QuestionRequest):
    future = Future()  # asyncio.Future
    request_queue.put({
        "account": req.account,
        "questions": req.questions,
        "future": future
    })
    result = await future  # Wait for result
    return result  # List of answers