import sqlalchemy as db
from sqlalchemy import (
    Column,
    UUID,
    VARCHAR,
    INTEGER,
    FLOAT,
    TIMESTAMP,
    BOOLEAN,
    TEXT,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "user"
    # id = Column(UUID, primary_key=True)
    username = Column(VARCHAR, nullable=False)
    password = Column(VARCHAR, nullable=False)


class Restaurant(Base):
    __tablename__ = "restaurant"
    # id = Column(UUID, primary_key=True)
    name = Column(VARCHAR, index=True)
    address = Column(VARCHAR)
    url = Column(VARCHAR)


class Comment(Base):
    __tablename__ = "comment"
    # id = Column(UUID, primary_key=True)
    content = Column(TEXT)
    rating = Column(FLOAT)
    model_prediction = Column(VARCHAR)
    need_review = Column(BOOLEAN)
    verified_result = Column(VARCHAR)
    report_comment = Column(TEXT)
    url = Column(VARCHAR)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship(User, foreign_keys=user_id)
    restaurant_id = Column(UUID, ForeignKey("restaurant.id"))
    restaurant = relationship(Restaurant, foreign_keys=restaurant_id)
