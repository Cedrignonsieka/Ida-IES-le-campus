from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ton_secret_key"

DATABASE = "database.db"

# Création de la table si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        dob = request.form['dob']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas !")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (fullname, email, password, dob, phone, address, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (fullname, email, hashed_password, dob, phone, address, gender))
            conn.commit()
            conn.close()
            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Cet email est déjà utilisé.")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            flash("Connexion réussie !")
            return redirect(url_for('register'))  # ou une page dashboard
        else:
            flash("Email ou mot de passe incorrect.")
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
