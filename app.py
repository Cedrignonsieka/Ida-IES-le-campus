from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key_123"  # à personnaliser

# -------------------------
# Base de données
# -------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Table utilisateurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        birthdate TEXT
    )
    """)

    # Table publications
    c.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        SELECT p.content, p.date, u.name 
        FROM publications p 
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC
    """)
    publications = [{"content": row[0], "date": row[1], "user_name": row[2]} for row in c.fetchall()]
    conn.close()

    return render_template("index.html", publications=publications)

# Inscription
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        name = request.form["name"]
        birthdate = request.form["birthdate"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password, name, birthdate) VALUES (?, ?, ?, ?)",
                      (email, password, name, birthdate))
            conn.commit()
        except sqlite3.IntegrityError:
            return "⚠️ Cet email est déjà utilisé."
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# Connexion
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id, password, name FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["user_name"] = user[2]
            return redirect(url_for("index"))
        else:
            return "⚠️ Email ou mot de passe incorrect."

    return render_template("login.html")

# Déconnexion
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

# Ajouter une publication
@app.route('/post', methods=["POST"])
def post():
    if "user_id" not in session:
        return redirect(url_for("login"))

    content = request.form["content"]
    date = request.form["date"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO publications (user_id, content, date) VALUES (?, ?, ?)",
              (session["user_id"], content, date))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# -------------------------
# Lancer l'app
# -------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
