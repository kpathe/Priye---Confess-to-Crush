from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

# Generate random names for confessions
def generate_random_name():
    adjectives = ['Brave', 'Mysterious', 'Clever', 'Shy', 'Curious', 'Gentle', 'Witty', 'Bold']
    nouns = ['Panda', 'Tiger', 'Eagle', 'Fox', 'Dolphin', 'Phoenix', 'Owl', 'Dragon']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"

# Database initialization
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS confessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                confession TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Add a confession
@app.route("/add", methods=["GET", "POST"])
def add_confession():
    if request.method == "POST":
        confession_text = request.form["confession"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_name = generate_random_name()

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO confessions (name, confession, timestamp)
                VALUES (?, ?, ?)
            ''', (random_name, confession_text, timestamp))
            conn.commit()

        return redirect(url_for("view_confessions"))

    return render_template("add.html")

# View all confessions
@app.route("/view")
def view_confessions():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT name, confession, timestamp FROM confessions ORDER BY id DESC')
        confessions = c.fetchall()

    return render_template("view.html", confessions=confessions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
