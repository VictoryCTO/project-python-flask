from app.extensions import db, bcrypt
from datetime import datetime

# Association table for the many-to-many relationship between users and roles
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.role_id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    inactivated_on = db.Column(db.DateTime, nullable=True)
    roles = db.relationship("Role", secondary=user_roles, back_populates="users")

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    department_name = db.Column(db.String(100), nullable=False)
    users = db.relationship("User", secondary=user_roles, back_populates="roles")

    __table_args__ = (
        db.UniqueConstraint("role_name", "department_name", name="uq_role_department"),
    )

    def __repr__(self):
        return f"<Role {self.role_name} in {self.department_name}>"
