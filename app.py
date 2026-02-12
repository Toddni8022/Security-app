import logging
from flask import Flask, request, jsonify
import os

# Basic logging setup
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            logging.warning("Invalid login attempt")
            return jsonify({'error': 'Invalid input'}), 400
        logging.info("User logged in")
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            logging.warning("Invalid input received")
            return jsonify({'error': 'Invalid input'}), 400
        logging.info("Data processed successfully")
        return jsonify({'message': 'Data received successfully'}), 200
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
