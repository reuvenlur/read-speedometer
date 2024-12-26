import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database_interface import get_connection, save_page_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PORT = int(os.getenv("BACKEND_PORT", 5000))
HOST = os.getenv("BACKEND_HOST", "0.0.0.0")

# Configure logging
logger = logging.getLogger('Application')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - Server.py - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Initialize Flask app and database connection
app = Flask(__name__)
CORS(app)
engine = get_connection()

# @app.route('/calculate_speed', methods=['POST'])
# def calculate_speed():
#     try:
#         raw_data = request.data.decode('utf-8')  # קבלת גוף הבקשה כטקסט
#         logger.info(f"Raw request data: {raw_data}")
#         return jsonify({"raw_request_data": raw_data}), 200
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         return jsonify({"error": str(e)}), 500



@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    try:
        logger.info("Received request to /calculate_speed")
        
        # Get data from the request
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        username = data.get('username', 'unknown')
        page_number = data.get('page')
        logger.info(f"Parsed page_number: {page_number}")
        time_spent = float(data.get('time_spent'))
        logger.info(f"Parsed time_spent: {time_spent}")
        word_count = int(data.get('word_count'))
        logger.info(f"Parsed word_count: {word_count}")

        if page_number is None or time_spent <= 0 or word_count <= 0:
            raise ValueError("Invalid data: Page number, time spent, and word count must be valid and greater than 0")

        # Calculate reading speed
        reading_speed = (word_count / time_spent) * 60
        logger.info(f"Calculated reading speed for user {username}: {reading_speed:.2f} WPM")

        # Save data to the database
        save_result = save_page_data(engine, username, page_number, time_spent, reading_speed)
        if 'error' in save_result:
            logger.error(f"Error saving data: {save_result['error']}")
            return jsonify(save_result), 500

        return jsonify({
            "reading_speed": round(reading_speed, 2),
            "save_message": save_result.get('message')
        }), 200

    except ValueError as ve:
        logger.warning(f"Value Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500