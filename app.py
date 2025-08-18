from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Pour autoriser les requêtes depuis ton frontend

# Infos de connexion PostgreSQL (Render)
DB_HOST = 'dpg-d2h1df7diees73e201jg-a.oregon-postgres.render.com'
DB_NAME = 'cedric_02bc'
DB_USER = 'cedric_02bc_user'
DB_PASS = 'K0a9OldVn97I9bhRoxxB2yuyxsepNqjF'
DB_PORT = '5432'

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# Route de test
@app.route('/')
def home():
    return "✅ Backend Flask + PostgreSQL fonctionne sur Render !"

# Route login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, mot_de_passe FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'success': False, 'message': 'Utilisateur non trouvé.'}), 401

        user_id, nom, mot_de_passe_en_base = user

        if password != mot_de_passe_en_base:
            return jsonify({'success': False, 'message': 'Mot de passe incorrect.'}), 401

        return jsonify({'success': True, 'message': f'Bienvenue {nom}', 'user_id': user_id})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erreur serveur : {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
