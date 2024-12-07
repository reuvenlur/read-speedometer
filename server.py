import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from database_interface import get_connection, save_page_data

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - Server.py - %(message)s')

# Initialize Flask app and database connection
app = Flask(__name__)
CORS(app)
engine = get_connection()

@app.route('/')
def home():
    logging.info("Server.py: Accessed home route")
    return "Welcome to the ReadSpeedometer API!"

@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    try:
        logging.info("Server.py: Received request to /calculate_speed")
        
        # Get data from the request
        data = request.get_json()
        username = data.get('username', 'unknown')
        page_number = data.get('page')
        time_spent = float(data.get('time_spent'))
        word_count = int(data.get('word_count'))

        if page_number is None or time_spent <= 0 or word_count <= 0:
            raise ValueError("Invalid data: Page number, time spent, and word count must be valid and greater than 0")

        # Calculate reading speed
        reading_speed = (word_count / time_spent) * 60
        logging.info(f"Server.py: Calculated reading speed for user {username}: {reading_speed:.2f} WPM")

        # Save data to the database
        save_result = save_page_data(engine, username, page_number, time_spent, reading_speed)
        if 'error' in save_result:
            logging.error(f"Server.py: Error saving data: {save_result['error']}")
            return jsonify(save_result), 500

        return jsonify({
            "reading_speed": round(reading_speed, 2),
            "save_message": save_result.get('message')
        }), 200

    except ValueError as ve:
        logging.warning(f"Server.py: Value Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Server.py: Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    try:
        logging.info("Server.py: Starting Flask server")
        app.run(debug=True)
    except Exception as e:
        logging.critical(f"Server.py: Critical error while starting server: {e}")
