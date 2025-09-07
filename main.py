from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

# Route d'accueil
@app.get("/")
def home():
    return {"message": "Bienvenue sur Debo 🎉, ton service est en ligne ✅"}

# Route pour générer des nombres aléatoires à partir d'une date
@app.get("/generate/{date_str}")
def generate(date_str: str):
    try:
        # Vérifier que la date est bien au format YYYY-MM-DD
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return {"error": "Format de date invalide. Utilise YYYY-MM-DD"}

    # Générer 3 blocs de 5 nombres entre 1 et 90
    blocs = []
    for _ in range(3):
        bloc = random.sample(range(1, 91), 5)
        blocs.append(bloc)

    return {"date": date_str, "blocs": blocs}
