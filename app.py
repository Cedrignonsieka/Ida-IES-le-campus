from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change ça pour plus de sécurité


# ---------------------------
# Initialisation de la base
# ---------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Table des utilisateurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birthdate TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Table des publications
    c.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------------------
# Routes principales
# ---------------------------
@app.route("/")
def index():
    if "user_id" in session:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            SELECT publications.content, publications.date, users.name
            FROM publications
            JOIN users ON publications.user_id = users.id
            ORDER BY publications.date DESC
        """)
        posts = c.fetchall()
        conn.close()
        return render_template("index.html", posts=posts, user=session["user_name"])
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, birthdate, email, password) VALUES (?, ?, ?, ?)",
                      (name, birthdate, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "❌ Cet email est déjà utilisé !"
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("index"))
        else:
            return "❌ Email ou mot de passe incorrect"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/post", methods=["POST"])
def post():
    if "user_id" in session:
        content = request.form["content"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO publications (user_id, content) VALUES (?, ?)", (session["user_id"], content))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


# ---------------------------
# Lancement local
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
