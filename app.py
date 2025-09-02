from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key_123"  # à changer en production

DB_NAME = "database.db"

# Création de la table users si elle n'existe pas
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nom TEXT,
                prenom TEXT,
                date_naissance TEXT,
                telephone TEXT
            )
        """)
        conn.commit()

init_db()

@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html")  # page après login
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        date_naissance = request.form.get("date_naissance")
        telephone = request.form.get("telephone")

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (email, password, nom, prenom, date_naissance, telephone)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (email, password, nom, prenom, date_naissance, telephone))
                conn.commit()
                flash("Inscription réussie ! Vous pouvez maintenant vous connecter.")
                return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email déjà utilisé !")
            return redirect(url_for("register"))

    return render_template("register.html")

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
                flash("Connexion réussie !")
                return redirect(url_for("index"))
            else:
                flash("Email ou mot de passe incorrect !")
                return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Vous êtes déconnecté.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
