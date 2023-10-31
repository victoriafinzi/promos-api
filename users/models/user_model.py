from users.users import Users
from flask import g


def create_user(data):
    g.db_session.add(data)
    g.db_session.commit()
    return data


def get_user(id):
    return g.db_session.query(Users).filter(Users.id == id).first()


def get_clients():
    return g.db_session.query(Users).filter(Users.user_type == "CLIENT").all()


def update_user(data):
    g.db_session.merge(data)
    g.db_session.commit()
    return data


def delete_user(id):
    from promos.promos import Promos
    g.db_session.query(Promos).filter(Promos.created_by == id).delete()
    g.db_session.query(Users).filter(Users.id == id).delete()
    g.db_session.commit()
    return f"User {id} deleted"
