import enum
from database import db
from sqlalchemy import Column, DateTime, Integer, Sequence, String, Enum
from sqlalchemy.orm import relationship


class UserType(enum.Enum):
    ADMIN = 0
    CLIENT = 1

class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    user_type = Column(Enum(UserType), nullable=False, default="CLIENT")
    password_reset_token = Column(String, unique=True)
    password_reset_token_expiration = Column(DateTime)
    
    user_promos = relationship('Promos', back_populates='user')