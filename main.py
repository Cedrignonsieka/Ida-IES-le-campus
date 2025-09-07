from fastapi import FastAPI, Query
import random
from datetime import datetime

app = FastAPI(title="Loterie Adaptée", description="Générateur de tirages basé sur la date (speed)")

def generate_lottery_draw(speed=None):
    """
    Génère un tirage adapté :
    - 5 numéros principaux uniques (1-90)
    - 1 numéro complémentaire (1-10)
    - Dépendance du 'speed'
    """
    main_numbers = []

    for i in range(5):
        options = set()
        # Option 1 : speed modulo 90
        if speed is not None:
            speed_num = ((speed - 1) % 90) + 1
            if speed_num not in main_numbers:
                options.add(speed_num)
        # Option 2 et 3 : nombres aléatoires uniques
        while len(options) < 3:
            rand_num = random.randint(1, 90)
            if rand_num not in main_numbers:
                options.add(rand_num)
        next_num = random.choice(list(options))
        main_numbers.append(next_num)
        speed = next_num

    random.shuffle(main_numbers)
    bonus_number = random.randint(1, 10)
    return main_numbers, bonus_number

@app.get("/generate")
def generate(date: str = Query(..., description="Date au format YYYYMMDD pour le speed")):
    """
    Génère 3 tirages basés sur la date (speed).
    Exemple : /generate?date=20250907
    """
    try:
        datetime.strptime(date, "%Y%m%d")
        speed_initial = int(date)
    except ValueError:
        return {"error": "Format de date invalide. Utilisez YYYYMMDD."}

    # Seed pour déterminisme
    random.seed(speed_initial)
    results = []
    for _ in range(3):
        mains, bonus = generate_lottery_draw(speed_initial)
        results.append({"numéros_principaux": mains, "numéro_complémentaire": bonus})
    return {"tirages": results}
