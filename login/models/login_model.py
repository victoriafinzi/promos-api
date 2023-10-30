from datetime import datetime, timedelta
from users.users import Users
from flask import g
import bcrypt
import secrets


def validate_login(username, password):
    user = g.db_session.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    else:
        return None


def generate_reset_token(user):
    password_reset_token = secrets.token_hex(16)
    password_reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
    
    user.password_reset_token = password_reset_token
    user.password_reset_token_expiration = password_reset_token_expiration

    g.db_session.merge(user)
    g.db_session.commit()

    return password_reset_token


def find_user_by_reset_token(password_reset_token):
    return g.db_session.query(Users).filter(Users.password_reset_token == password_reset_token).first()


def is_reset_token_expired(user_id):
    user = g.db_session.query(Users).filter(Users.id == user_id).first()

    if user.password_reset_token_expiration is None:
        return True
    
    current_time = datetime.utcnow()
    return current_time > user.password_reset_token_expiration
