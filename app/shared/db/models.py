from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass

model_config = ConfigDict(
    extra='allow',
    from_attributes=True)


@dataclass(config=model_config) 
class CommentUpdate(BaseModel):
    id: UUID
    content: Optional[str] = None
    rating: Optional[float] = None
    model_prediction: Optional[str] = None
    need_review: Optional[bool] = None
    verified_result: Optional[str] = None
    report_comment: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[UUID] = None
    restaurant_id: Optional[UUID] = None

    class Config:
        orm_mode = True
        from_attributes = True
