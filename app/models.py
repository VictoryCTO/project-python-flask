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


class UserActiveStatusChange(db.Model):
    __tablename__ = "users_active_status_changes"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="inactive")
    date = db.Column(db.DateTime, default=utc_now)
    user = db.relationship("User", backref="status_changes")


"""Allow for the creation of one or more roles with attributes
role_id, role_name, and department_name.
Combination of role_name and department_name is unique
Allow for a user to be assigned one or more roles
and for a role to be assigned to one or more users.
Users_roles table relies on roles_lookup
for putting a name and dept to a role id."""


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)  # Issue 02-Active users
    access_level = db.Column(
        db.String(16), default="basic", nullable=False
    )  # Kept as requested

    # Establish the many-to-many relationship with roles
    roles = db.relationship(
        "RolesLookup", secondary="users_roles", back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class UserRole(db.Model):
    __tablename__ = "users_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles_lookup.id"), nullable=False)

    # Add unique constraint to prevent duplicate user-role assignments
    __table_args__ = (db.UniqueConstraint("user_id", "role_id", name="_user_role_uc"),)


class RolesLookup(db.Model):
    __tablename__ = "roles_lookup"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16), nullable=False)
    department_name = db.Column(db.String(64), nullable=False)

    # Establish the many-to-many relationship with users
    users = db.relationship("User", secondary="users_roles", back_populates="roles")

    # Unique constraint on role_name and department_name
    __table_args__ = (
        db.UniqueConstraint("role_name", "department_name", name="_role_dept_uc"),
    )

    def __repr__(self):
        return f"<RolesLookup {self.role_name} - {self.department_name}>"
