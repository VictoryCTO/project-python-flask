from ..models import User
from ..extensions import db, bcrypt


def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered", "username": new_user.username}


def check_password(email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        pass
        # print(f"found user: {user.username}")
        # print(f"email: {email}")
        # print(f"password: {password}")
        # print(f"db password: {user.password}")
    else:
        print("user not found")

    if user.password == password:
        return True
    else:
        return False
