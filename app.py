from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Helper function to generate random usernames
def generate_username():
    adjectives = ['Mystic', 'Anonymous', 'Silent', 'Clever', 'Brave', 'Shy', 'Hidden', 'Mysterious']
    nouns = ['Shadow', 'Penguin', 'Fox', 'Tiger', 'Wizard', 'Knight', 'Dragon', 'Whale']
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 999)}"

# Initialize the database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS confessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                username TEXT NOT NULL
            )
        """)
        conn.commit()

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Submit Confession
@app.route('/submit', methods=['GET', 'POST'])
def submit_confession():
    if request.method == 'POST':
        content = request.form.get('content')
        if not content.strip():
            flash("Confession cannot be empty!", "error")
            return redirect(url_for('submit_confession'))

        # Generate timestamp and username
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        username = generate_username()

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO confessions (content, created_at, username) VALUES (?, ?, ?)",
                (content, timestamp, username)
            )
            conn.commit()
        flash("Confession submitted successfully!", "success")
        return redirect(url_for('index'))
    return render_template('submit.html')

# View Confessions
@app.route('/view')
def view_confessions():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM confessions ORDER BY id DESC")
        confessions = cursor.fetchall()
    return render_template('view.html', confessions=confessions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
