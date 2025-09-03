import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ma_cle_ultra_secrete"  # change ça par une clé forte

# ============================
# 🔗 Connexion à la base Render PostgreSQL
# ============================
DB_HOST = "dpg-d2s2u763jp1c738q696g-a.oregon-postgres.render.com"
DB_NAME = "database_db_gwev"
DB_USER = "database_db_gwev_user"
DB_PASS = "dniwpxker5BYw9a9rhN1zcHtlARyUZzw"
DB_PORT = "5432"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# ============================
# 🔧 Création des tables au démarrage
# ============================
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Table des utilisateurs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fullname TEXT,
            birthdate DATE
        );
    """)

    # Table des publications
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# ============================
# 🌍 Routes Flask
# ============================

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT posts.content, users.fullname, posts.created_at
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
    """)
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        birthdate = request.form["birthdate"]

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (fullname, email, password, birthdate) VALUES (%s, %s, %s, %s)",
                (fullname, email, password, birthdate),
            )
            conn.commit()
        except Exception as e:
            print("Erreur enregistrement:", e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password, fullname FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["fullname"] = user[2]
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/post", methods=["POST"])
def post():
    if "user_id" not in session:
        return redirect(url_for("login"))

    content = request.form["content"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s)", (session["user_id"], content))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))

# ============================
# 🚀 Lancement de l’app
# ============================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
