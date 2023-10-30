from database import db
from sqlalchemy import Column, DateTime, Integer, Sequence, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Promos(db.Model):
    def __init__(self, id, created_by, product_name, price, discount, expiration_date, description):
        self.id = id
        self.created_by = created_by
        self.product_name = product_name
        self.price = price
        self.discount = discount
        self.expiration_date = expiration_date
        self.description = description
        self.discounted_price = round(price * (1 - discount / 100), 2)
        
    __tablename__ = 'promos'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    create_date = Column(DateTime, nullable=False, default=func.now())
    expiration_date = Column(DateTime, nullable=False)
    description = Column(String)

    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('Users', back_populates='user_promos')