from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = "database.db"

# Connexion à SQLite et création de la table si elle n'existe pas
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT
            )
        """)
        db.commit()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Page d'accueil : liste des utilisateurs
@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT id, nom FROM utilisateurs")
    utilisateurs = cur.fetchall()
    return render_template("index.html", utilisateurs=utilisateurs)

# Ajouter un utilisateur
@app.route("/add", methods=["POST"])
def add_user():
    nom = request.form.get("nom")
    db = get_db()
    db.execute("INSERT INTO utilisateurs (nom) VALUES (?)", (nom,))
    db.commit()
    return "<p>Utilisateur ajouté !</p><a href='/'>Retour</a>"

# Lancer l’application sur Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
