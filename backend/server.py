# import logging
import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from database_interface import get_connection, save_page_data, read_table_data, delete_all_data
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PORT = int(os.getenv("BACKEND_PORT", 5000))
HOST = os.getenv("BACKEND_HOST", "0.0.0.0")

import logging

# Set up logger
logger = logging.getLogger('flask_logger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Configure logging
# logger = logging.getLogger('Application')
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - [MY_LOG] - %(message)s')

# StreamHandler for console logging
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# FileHandler for logging to a file
# file_handler = logging.FileHandler('combined_logs.log')
# file_handler = logging.FileHandler('/path/to/logs/combined_logs.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# Initialize Flask app and database connection
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
# session.permanent = True
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
engine = get_connection()

# Test database connection before starting the app
try:
    connection = engine.connect()
    # logger.info("[MY_LOG] Database connected successfully.")
    connection.close()
except Exception as e:
    # logger.error(f"[MY_LOG] Database connection failed: {e}")
    pass

@app.route('/save_username_in_session', methods=['OPTIONS', 'POST'])
def save_username_in_session():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 204
    try:
        data = request.get_json()
        logger.debug(f"data: {data}")
        # print(data)  # הדפסת הנתונים
        username = data.get('username')
        logger.debug(f"username: {username}")
        if not username:
            raise ValueError("Username is required")
         # שמירת שם המשתמש בקובץ
        with open('/app/username.txt', 'w') as file:
            file.write(username)

        # session['username'] = username
        # logger.debug(f"Session username: {session.get('username')}")
        # session.modified = True
        # logger.debug(f"Session2 username: {session.get('username')}")
        # print(f"Session username: {session.get('username')}")
        # logger.info(f"[MY_LOG] Username saved in session: {session.get('username', 'unknown')}")
        return jsonify({'message': f'Username {username} saved successfully'}), 200
    except ValueError as ve:
        # logger.warning(f"[MY_LOG] Input error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # logger.error(f"[MY_LOG] Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# @app.route('/log', methods=['POST'])
# def log_from_frontend():
#     try:
#         data = request.get_json()
#         level = data.get('level', 'INFO').upper()
#         message = data.get('message', '')

#         if not message:
#             raise ValueError("Message is required for logging.")

#         # Map log levels to logger methods
#         log_methods = {
#             'DEBUG': None,  # logger.debug,
#             'INFO': None,  # logger.info,
#             'WARNING': None,  # logger.warning,
#             'ERROR': None,  # logger.error,
#             'CRITICAL': None,  # logger.critical,
#         }

#         # Log the message using the appropriate level
#         log_method = log_methods.get(level, None)  # logger.info
#         # log_method(f"[FRONTEND_LOG] {message}")

#         return jsonify({"message": "Log recorded successfully"}), 200
#     except ValueError as ve:
#         # logger.warning(f"[MY_LOG] Input error: {ve}")
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         # logger.error(f"[MY_LOG] Unexpected error: {e}")
#         return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    try:
        # logger.info("[MY_LOG] Processing speed calculation request...")
        # username = session.get('username', 'unknown')
        # logger.debug(f"Session username: {username}")

        try:
            with open('/app/username.txt', 'r') as file:
                username = file.read().strip()
        except FileNotFoundError:
            username = 'unknown'  # אם הקובץ לא נמצא

        data = request.get_json()
        page_number = data.get('page')
        time_spent = float(data.get('time_spent'))
        word_count = int(data.get('word_count'))

        if page_number is None or time_spent <= 0 or word_count <= 0:
            raise ValueError("Invalid data: Page number, time spent, and word count must be valid and greater than 0")

        reading_speed = (word_count / time_spent) * 60
        # logger.info(f"[MY_LOG] Reading speed for user {username}: {reading_speed:.2f} WPM")

        save_result = save_page_data(engine, username, page_number, time_spent, reading_speed)
        if 'error' in save_result:
            # logger.error(f"[MY_LOG] Error saving data: {save_result['error']}")
            return jsonify(save_result), 500

        return jsonify({
            "reading_speed": round(reading_speed, 2),
            "save_message": save_result.get('message')
        }), 200
    except ValueError as ve:
        # logger.warning(f"[MY_LOG] Input error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # logger.error(f"[MY_LOG] Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        data = read_table_data(engine)
        if "error" in data:
            # logger.error(f"[MY_LOG] Error fetching data: {data['error']}")
            return jsonify({"error": "Failed to fetch data"}), 500
        return jsonify(data), 200
    except Exception as e:
        # logger.error(f"[MY_LOG] Unexpected error while fetching data: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/delete_all_data', methods=['OPTIONS', 'POST'])
def delete_all_data_route():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 204
    try:
        # logger.info("[MY_LOG] Processing delete all data request...")
        result = delete_all_data(engine)
        if 'error' in result:
            # logger.error(f"[MY_LOG] Error deleting data: {result['error']}")
            return jsonify(result), 500
        # logger.info("[MY_LOG] All data deleted successfully.")
        return jsonify(result), 200
    except Exception as e:
        # logger.error(f"[MY_LOG] Unexpected error during data deletion: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # logger.info("[MY_LOG] Starting application...")
    app.run(host=HOST, port=PORT, debug=True)
