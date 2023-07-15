from typing import Union
import jwt
import uvicorn

from fastapi import FastAPI, Depends
from shared.db.repo import BaseRepo
from shared.db.schemas import Comment
from shared.db.models import CommentUpdate, CommentOut
from .request import LoginRequest, CommentReviewRequest

from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .security import validate_token
from fastapi.middleware.cors import CORSMiddleware

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'
app = FastAPI()
repo = BaseRepo()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3  # Expired after 3 days
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(username, password):
    user = repo.get_user(username, password)
    if user:
        return True
    return False


@app.get(
    "/api/comment-mismatch-prediction/skip/{skip}/limit/{limit}",
    dependencies=[Depends(validate_token)])
def read_need_review(skip: int, limit: int) -> Any:
    [data, total] = repo.get_comments_mismatch_prediction(skip, limit)
    return {
        "data": data,
        "total": total
    }


@app.post(
    "/api/comment/review",
    dependencies=[Depends(validate_token)])
def update_review(request_data: CommentReviewRequest):
    comment = repo.get_comment(request_data.id)
    comment_in: CommentUpdate = CommentUpdate.from_orm(comment)

    if comment_in:
        comment_in.verified_result = request_data.verified_result
        comment_in.report_comment = request_data.report_comment
        comment_in.need_review = False
        repo.update_comment(comment_in)


@app.post('/api/login')
def login(request_data: LoginRequest):
    if verify_password(username=request_data.username, password=request_data.password):
        token = generate_token(request_data.username)
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
