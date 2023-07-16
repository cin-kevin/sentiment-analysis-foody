from shared.db import engine
from shared.db.models import CommentOut, CommentUpdate
from shared.db.schemas import Comment, Restaurant, User
from shared.utils import get_uuid
from sqlalchemy.orm import Session, sessionmaker


class BaseRepo:
    def __init__(self, engine_in=None) -> None:
        session: Session = None
        if not engine_in:
            session = sessionmaker(bind=engine)
        else:
            session = sessionmaker(bind=engine_in)
        self._session: Session = session()

    def get_user(self, username: str, password: str) -> User:
        with self._session as ss:
            user = (
                ss.query(User)
                .filter(User.username == username and User.password == password)
                .first()
            )
            return user

    def insert_restaurant(self, restaurant: Restaurant) -> Restaurant:
        with self._session as ss:
            # restaurant.id = get_uuid()
            ss.add(restaurant)
            ss.commit()
            return restaurant

    def insert_comment(self, comment: Comment) -> CommentOut:
        with self._session as ss:
            # comment.id = get_uuid()
            ss.add(comment)
            ss.commit()
            return CommentOut.from_orm(comment)

    def update_comment(self, comment_in: CommentUpdate) -> CommentOut:
        with self._session as ss:
            comment = ss.query(Comment).filter(Comment.id == comment_in.id).first()
            obj_data = comment.as_dict()
            update_data = comment_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(comment, field, update_data[field])

            ss.commit()
            return CommentOut.from_orm(comment)

    def get_comment(self, commentid) -> CommentOut:
        with self._session as ss:
            cmt = ss.query(Comment).filter(Comment.id == commentid).first()
            return CommentOut.from_orm(cmt)

    def get_comments_to_predict(self, skip: int, limit: int) -> list[CommentOut]:
        with self._session as ss:
            comments = (
                ss.query(Comment)
                .filter(Comment.model_prediction == None)
                .offset(skip)
                .limit(limit)
                .all()
            )
            commentouts: list[CommentOut] = []
            for comment in comments:
                commentout = CommentOut.from_orm(comment)
                commentouts.append(commentout)

            return commentouts

    def get_comments_mismatch_prediction(
        self, skip: int, limit: int
    ) -> list[CommentOut]:
        with self._session as ss:
            comments: list[Comment] = (
                ss.query(Comment)
                .filter(Comment.need_review == True)
                .order_by(Comment.restaurant_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            total = ss.query(Comment).filter(Comment.need_review == True).count()

            commentouts: list[CommentOut] = []
            for comment in comments:
                commentout = CommentOut.from_orm(comment)
                commentouts.append(commentout)

            return [commentouts, total]
