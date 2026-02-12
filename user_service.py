from flask import Blueprint, request, jsonify
import os
import logging

user_auth = Blueprint('user_auth', __name__)

API_KEY = os.getenv('API_KEY')

@user_auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            logging.warning("Invalid login attempt")
            return jsonify({'error': 'Invalid input'}), 400
        # Authenticate user (placeholder)
        logging.info("User logged in")
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
