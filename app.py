from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'database.db'

# Vérifie si la DB existe, sinon la crée
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Base de données créée avec succès !")

# Appelle la fonction au démarrage
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    utilisateurs = cursor.fetchall()
    conn.close()
    return render_template("index.html", utilisateurs=utilisateurs)

@app.route('/add', methods=['POST'])
def add_utilisateur():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    if nom and prenom:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO utilisateurs (nom, prenom) VALUES (?, ?)", (nom, prenom))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
