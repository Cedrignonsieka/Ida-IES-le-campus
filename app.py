from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ton_secret_key"  # Change ceci par un secret fort

# Création de la table users si elle n'existe pas
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Page d'accueil protégée
@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html", email=session["user_email"])
    else:
        return redirect(url_for("login"))

# Inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            conn.close()
            flash("Compte créé avec succès ! Connectez-vous.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Cet email existe déjà.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

# Connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["user_email"] = email
            flash("Connecté avec succès !", "success")
            return redirect(url_for("index"))
        else:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    flash("Déconnecté.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
