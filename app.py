import psycopg2
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "ma_clé_secrète"  # ⚠️ change ça par une vraie clé secrète

# ==========================
# 1. Connexion PostgreSQL Render
# ==========================
DATABASE_URL = "postgresql://database_db_gwev_user:dniwpxker5BYw9a9rhN1zcHtlARyUZzw@dpg-d2s2u763jp1c738q696g-a.oregon-postgres.render.com/database_db_gwev"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

# ==========================
# 2. Création des tables
# ==========================
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Table utilisateurs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        birthdate DATE,
        bio TEXT
    );
    """)

    # Table publications
    cur.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        content TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

# ==========================
# 3. Routes Flask
# ==========================
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.content, p.date, u.name
        FROM publications p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC;
    """)
    publications = cur.fetchall()
    conn.close()

    return render_template("index.html", publications=publications)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        birthdate = request.form.get("birthdate")
        bio = request.form.get("bio")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password, birthdate, bio) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, password, birthdate, bio))
        conn.commit()
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
        cur.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["name"] = user[1]
            return redirect(url_for("index"))
        else:
            return "Identifiants invalides."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/publish", methods=["POST"])
def publish():
    if "user_id" not in session:
        return redirect(url_for("login"))

    content = request.form["content"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO publications (user_id, content) VALUES (%s, %s)", (session["user_id"], content))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
