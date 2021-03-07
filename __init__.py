from db import db
from flask import Flask


def create_app():
    app = Flask()
    db.init_app(app)

    from user_model import User
    with app.app_context():
        db.create_all()
