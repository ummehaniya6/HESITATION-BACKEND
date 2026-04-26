import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delay REAL,
            result TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def track_click(delay, hesitation, current_clock):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interactions (delay, result, time) VALUES (?, ?, ?)",
                   (delay, hesitation, current_clock))
    conn.commit()
    conn.close()
    
    return jsonify({
        "delay": delay,
        "result": hesitation,
        "time": current_clock
    })

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    delay = data.get('delay', 0)
    hesitation = data.get('result', 'unknown')
    current_clock = data.get('time', '00:00:00')
    return track_click(delay, hesitation, current_clock)

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/')
def home():
    return "Backend is running successfully 😊"

if __name__ == "__main__":
    app.run(debug=True)