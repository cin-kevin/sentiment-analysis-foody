from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass

model_config = ConfigDict(extra="allow", from_attributes=True)


@dataclass(config=model_config)
class CommentUpdate(BaseModel):
    id: Optional[int] = None
    content: Optional[str] = None
    rating: Optional[float] = None
    model_prediction: Optional[str] = None
    need_review: Optional[bool] = None
    verified_result: Optional[str] = None
    report_comment: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    restaurant_id: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True


@dataclass(config=model_config)
class CommentOut(BaseModel):
    id: int
    content: Optional[str] = None
    rating: Optional[float] = None
    model_prediction: Optional[str] = None
    need_review: Optional[bool] = None
    verified_result: Optional[str] = None
    report_comment: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    restaurant_id: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True
