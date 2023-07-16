from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class CommentReviewRequest(BaseModel):
    id: int
    verified_result: str
    report_comment: Optional[str]
