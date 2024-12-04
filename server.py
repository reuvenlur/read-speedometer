from flask import Flask, request, jsonify

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
