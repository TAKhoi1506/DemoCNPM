from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from saleapp import app, db
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime

class UserEnum(RoleEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(200), default="https://res.cloudinary.com/dy1unykph/image/upload/v1729842193/iPhone_15_Pro_Natural_1_ltf9vr.webp")
    role = Column(Enum(UserEnum), default=UserEnum.USER)
    # receipts = relationship('Receipt', backref='user', lazy=True)
    # comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        self.name


class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    rooms = relationship('Room', backref='roomType', lazy=True)

    def __str__(self):
        return self.name


class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(200), default="https://res.cloudinary.com/dy1unykph/image/upload/v1729842193/iPhone_15_Pro_Natural_1_ltf9vr.webp")
    roomType_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    active = Column(Boolean, default=True)
    # details = relationship('ReceiptDetail', backref='room', lazy=True)
    # comments = relationship('Comment', backref='room', lazy=True)

    def __str__(self):
        return self.name


# class Base(db.Model):
#     __abstract__ = True
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     active = Column(Boolean, default=True)
#     created_date = Column(DateTime, default=datetime.now())
#
#
# class Receipt(Base):
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     details = relationship('ReceiptDetail', backref="receipt", lazy=True)
#
#
# class ReceiptDetail(Base):
#     quantity = Column(Integer, default=0)
#     unit_price = Column(Float, default=0.0)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
#
#
# class Comment(Base):
#     content = Column(String(255), nullable=False)
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        # c1 = RoomType(name="Single")
        # c2 = RoomType(name="Double")
        # c3 = RoomType(name="Deluxe")
        # c4 = RoomType(name="Family")
        # db.session.add_all([c1,c2,c3,c4])
        # db.session.commit()
        # import json
        # with open('data/rooms.json', encoding='utf-8') as f:
        #     rooms = json.load(f)
        #     for p in rooms:
        #         prod = Room(**p)
        #         db.session.add(prod)

        import hashlib

        password = str(hashlib.md5("123".encode('utf-8')).hexdigest())

        u = User(name="khoi", username="user", password=password)
        u2 = User(name="khoi", username="admin", password=password, role=UserEnum.ADMIN)
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

