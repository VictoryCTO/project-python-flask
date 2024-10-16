from app.extensions import db, bcrypt
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    inactivated_on = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(50), nullable=False, default="user")

    def __repr__(self):
        return f"<User {self.username}>"
