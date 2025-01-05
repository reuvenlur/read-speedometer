import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from DB_operations import get_connection, save_page_data, read_table_data, delete_all_data
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Enable CORS for specific origin
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Establish database connection
engine = get_connection()

# Test the database connection before starting the app
try:
    connection = engine.connect()
    connection.close()
except Exception:
    pass

# Route to save the username in the session
@app.route('/save_username_in_session', methods=['OPTIONS', 'POST'])
def save_username_in_session():
    # Handle pre-flight request for CORS
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 204
    
    try:
        # Get the data from the request
        data = request.get_json()
        username = data.get('username')
        
        # Ensure username is provided
        if not username:
            raise ValueError("Username is required")
        
        # Save username to a file (this replaces session-based storage)
        with open('/app/username.txt', 'w') as file:
            file.write(username)

        return jsonify({'message': f'Username {username} saved successfully'}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

# Route to calculate reading speed
@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    try:
        # Read username from file
        try:
            with open('/app/username.txt', 'r') as file:
                username = file.read().strip()
        except FileNotFoundError:
            username = 'unknown'  # Default to 'unknown' if username is not found

        # Get data from the request
        data = request.get_json()
        page_number = data.get('page')
        time_spent = float(data.get('time_spent'))
        word_count = int(data.get('word_count'))

        # Validate the data
        if page_number is None or time_spent <= 0 or word_count <= 0:
            raise ValueError("Invalid data")

        # Calculate the reading speed
        reading_speed = (word_count / time_spent) * 60
        
        # Save the calculated reading speed to the database
        save_result = save_page_data(engine, username, page_number, time_spent, reading_speed)
        if 'error' in save_result:
            return jsonify(save_result), 500

        return jsonify({
            "reading_speed": round(reading_speed, 2),
            "save_message": save_result.get('message')
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

# Route to get all data from the database
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    try:
        # Fetch all data from the database
        data = read_table_data(engine)
        if "error" in data:
            return jsonify({"error": "Failed to fetch data"}), 500
        return jsonify(data), 200
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

# Route to delete all data from the database
@app.route('/delete_all_data', methods=['OPTIONS', 'POST'])
def delete_all_data_route():
    # Handle pre-flight request for CORS
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 204
    
    try:
        # Delete all data from the database
        result = delete_all_data(engine)
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host=os.getenv("BACKEND_HOST", "0.0.0.0"), port=int(os.getenv("BACKEND_PORT", 5000)), debug=True)
