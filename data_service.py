from flask import Blueprint, request, jsonify
import logging

data_processing = Blueprint('data_processing', __name__)

@data_processing.route('/data', methods=['POST'])
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
