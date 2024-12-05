from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS library

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# מסלול ברירת מחדל
@app.route('/')
def home():
    return "Welcome to the ReadSpeedometer API!"

# מסלול לשמירת נתוני עמוד
@app.route('/save_page_data', methods=['POST'])
def save_page_data():
    data = request.get_json()  # קבלת נתונים כ-JSON
    page = data.get('page')
    time_spent = data.get('time_spent')
    word_count = data.get('word_count')

    # בדיקת תקינות נתונים
    if not page or time_spent is None or word_count is None:
        return jsonify({'error': 'Missing data'}), 400

    # הדפסת הנתונים לטרמינל (נשפר זאת בהמשך)
    print(f"Page: {page}, Time Spent: {time_spent}s, Word Count: {word_count}")

    return jsonify({'message': 'Page data saved successfully!'}), 200

@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    try:
        data = request.get_json()
        print(f"Received data: {data}")

        # המרת נתונים למספרים
        time_spent = float(data.get('time_spent'))
        word_count = int(data.get('word_count'))

        # בדיקה אם הנתונים תקינים
        if time_spent <= 0 or word_count <= 0:
            raise ValueError("Time spent and word count must be greater than 0")

        # חישוב מהירות קריאה
        reading_speed = (word_count / time_spent) * 60
        return jsonify({"reading_speed": round(reading_speed, 2)}), 200
    except ValueError as ve:
        print(f"Value Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
