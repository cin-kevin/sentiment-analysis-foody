from shared.db.schemas import User, Restaurant, Comment
from shared.db.models import CommentUpdate
from shared.db import engine
from sqlalchemy.orm import sessionmaker, Session
from shared.utils import get_uuid


class BaseRepo:
    def __init__(self) -> None:
        session: Session = sessionmaker(bind=engine)
        self._session: Session = session()

    def insert_restaurant(self, restaurant: Restaurant) -> Restaurant:
        with self._session as ss:
            restaurant.id = get_uuid()
            ss.add(restaurant)
            ss.commit()
            return restaurant

    def insert_comment(self, comment: Comment) -> Comment:
        with self._session as ss:
            comment.id = get_uuid()
            ss.add(comment)
            ss.commit()
            return comment

    def update_comment(self, comment_in: CommentUpdate) -> Comment:
        with self._session as ss:
            comment = (
                ss.query(Comment)
                .filter(Comment.id == comment_in.id)
                .first()
            )
            obj_data = comment.as_dict()
            update_data = comment_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(comment, field, update_data[field])

            ss.commit()
            ss.refresh(comment)
            return comment

    def get_comment(self, commentid) -> Comment:
        with self._session as ss:
            return (
                ss.query(Comment)
                .filter(Comment.id == commentid)
                .first()
            )

    def get_comments_mismatch_prediction(
        self,
        skip: int,
        limit: int
    ) -> list[Comment]:
        with self._session as ss:
            comments = (
                ss.query(Comment).filter(Comment.need_review is True)
                .offset(skip)
                .limit(limit).all()
            )
            return comments
