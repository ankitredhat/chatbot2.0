from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create the table if it doesn't exist
def init_db():
    conn = sqlite3.connect('ngo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        location TEXT,
        message TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    location = data.get("location")
    message = data.get("message")

    conn = sqlite3.connect('ngo.db')
    c = conn.cursor()
    c.execute("INSERT INTO queries (name, phone, location, message) VALUES (?, ?, ?, ?)",
              (name, phone, location, message))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "reply": "✅ Thanks! We'll connect you with a nearby NGO soon."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

