from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    message = request.form['message']

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, phone, address, message) VALUES (?, ?, ?, ?)",
                  (name, phone, address, message))
        conn.commit()

    return render_template('thankyou.html')

@app.route('/dashboard')
def dashboard():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM messages")
        messages = c.fetchall()
    return render_template('dashboard.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
