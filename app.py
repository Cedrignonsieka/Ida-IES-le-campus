from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ton_secret_key"  # Change ça pour quelque chose de fort

DB_NAME = "database.db"

# Fonction pour créer la table users si elle n'existe pas
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

# Page d'accueil (protégée)
@app.route("/")
def index():
    if "user_id" in session:
        return f"Bienvenue ! Vous êtes connecté avec l'ID {session['user_id']}."
    return redirect(url_for("login"))

# Page d'inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
                conn.commit()
            flash("Inscription réussie ! Connectez-vous.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Cet email existe déjà.", "error")
    return render_template("register.html")

# Page de connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            flash("Connexion réussie !", "success")
            return redirect(url_for("index"))
        else:
            flash("Email ou mot de passe incorrect.", "error")

    return render_template("login.html")

# Déconnexion
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
