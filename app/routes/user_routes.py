from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db
from ..services.user_service import create_user, check_password

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = create_user(username, email, password)
    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if check_password(email, password) is True:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    
    
    # if user:
    #     print(f"Found user: {user.username}")
    #     print(f"Password: {password}")
    # else:
    #     print("User not found")

    # if user and user.check_password(user,):
    #     print("Password is correct")
    #     return jsonify({'message': 'Login successful', 'user': user.username}), 200
    # else:
    #     print("Password is incorrect or user not found")
    #     return jsonify({'message': 'Invalid credentials'}), 401


@user_bp.route('/profile', methods=['GET'])
def profile():
    # Dummy profile route for the user
    # In a real system, you would have authentication and user session handling
    return jsonify({'message': 'User profile information'}), 200