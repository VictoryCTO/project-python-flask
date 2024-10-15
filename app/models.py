from app.extensions import db
from datetime import datetime, tzinfo, timedelta


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


def utc_now():
    return datetime.now(UTC())


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)  # Issue 02-Active users

    def __repr__(self):
        return f"<User {self.username}>"


class UserActiveStatusChange(db.Model):
    __tablename__ = "users_active_status_changes"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="inactive")
    date = db.Column(db.DateTime, default=utc_now)
    user = db.relationship("User", backref="status_changes")
