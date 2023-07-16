from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
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
