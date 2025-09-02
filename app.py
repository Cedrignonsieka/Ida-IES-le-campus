from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"

# Connexion à SQLite et création de la table si elle n'existe pas
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Création automatique de la table utilisateurs
        db.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT
            )
        """)
        db.commit()
    return db

# Fermer la connexion après chaque requête
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Page d’accueil : liste des utilisateurs
@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT id, nom FROM utilisateurs")
    users = cur.fetchall()
    return render_template("index.html", users=users)

# Ajouter un utilisateur
@app.route("/add", methods=["POST"])
def add_user():
    nom = request.form.get("nom")
    db = get_db()
    db.execute("INSERT INTO utilisateurs (nom) VALUES (?)", (nom,))
    db.commit()
    return "<p>Utilisateur ajouté !</p><a href='/'>Retour</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
