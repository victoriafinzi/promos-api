import os
import sys
from dotenv import load_dotenv
from flask import Flask, g
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from database import init_db
from users.routes.user_routes import BLUEPRINT as user_blueprint
from promos.routes.promo_routes import BLUEPRINT as promo_blueprint
from login.routes.login_routes import BLUEPRINT as login_blueprint


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)
db = init_db(app)

@app.before_request
def before_request():
    g.db_session = db.session()

@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()

app.register_blueprint(user_blueprint)
app.register_blueprint(promo_blueprint)
app.register_blueprint(login_blueprint)

if __name__ == "__main__":
    if sys.platform.startswith('darwin'):
        app.run(host='0.0.0.0', port=8080)
    else:
        app.run()
    
