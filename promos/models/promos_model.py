from promos.promos import Promos
from flask import g

def create_promo(data):
    g.db_session.add(data)
    g.db_session.commit()
    return data


def get_promo(id):
    return g.db_session.query(Promos).filter(Promos.id == id).first()


def get_all_promos():
    return g.db_session.query(Promos).all()

def update_promo(data):
    g.db_session.merge(data)
    g.db_session.commit()
    return data


def delete_promo(id):
    g.db_session.query(Promos).filter(Promos.id == id).delete()
    g.db_session.commit()
    return f"Promo {id} deleted"