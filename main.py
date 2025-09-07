from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import random
from datetime import datetime
from fastapi.routing import APIRoute

app = FastAPI()

# Fonction pour générer les tirages
def generate_lottery_draw(speed=None):
    main_numbers = []
    for i in range(5):
        options = set()
        if speed is not None:
            speed_num = ((speed - 1) % 90) + 1
            if speed_num not in main_numbers:
                options.add(speed_num)
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

# Template HTML commun
def base_html(content):
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ida IES Le Campus</title>
    <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f2f5; }}
    .nav {{ margin-bottom: 20px; }}
    .nav button {{ padding: 10px 20px; margin-right: 10px; border: none; border-radius: 5px; background: #007bff; color: white; cursor: pointer; }}
    .nav button:hover {{ background: #0056b3; }}
    .container {{ max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
    input[type="text"] {{ width: 100%; padding: 8px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; }}
    button.submit {{ width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }}
    button.submit:hover {{ background: #218838; }}
    .result {{ margin-top: 20px; }}
    .numbers {{ display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }}
    .number-circle {{ width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #007bff; color: white; font-weight: bold; }}
    .bonus {{ background: #dc3545 !important; }}
    footer {{ text-align: center; margin-top: 40px; color: #666; }}
    </style>
    </head>
    <body>
    <div class="nav">
        <form method="get" action="/">
            <button type="submit">ACCUEIL</button>
        </form>
        <form method="get" action="/verifier">
            <button type="submit">VÉRIFIER</button>
        </form>
    </div>
    {content}
    <footer>© 2025 Ida IES Le Campus</footer>
    </body>
    </html>
    """

# Page d'accueil
@app.get("/", response_class=HTMLResponse)
async def home():
    content = "<div class='container'><h2>Bienvenue sur le site de tirages</h2><p>Cliquez sur VÉRIFIER pour générer vos tirages.</p></div>"
    return base_html(content)

# Page Vérifier avec le générateur
@app.get("/verifier", response_class=HTMLResponse)
async def verifier_get():
    content = """
    <div class='container'>
    <h2>Générateur de tirages</h2>
    <form method="post">
        <label>Entrez la date (YYYYMMDD) :</label>
        <input type="text" name="date_input" required>
        <button type="submit" class="submit">Générer tirages</button>
    </form>
    <div class="result"></div>
    </div>
    """
    return base_html(content)

@app.post("/verifier", response_class=HTMLResponse)
async def verifier_post(date_input: str = Form(...)):
    results_html = ""
    try:
        speed_initial = int(date_input)
        datetime.strptime(date_input, "%Y%m%d")
        random.seed(speed_initial)
        tirages = []
        for i in range(3):
            mains, bonus = generate_lottery_draw(speed_initial)
            main_circles = " ".join(f'<div class="number-circle">{n}</div>' for n in mains)
            bonus_circle = f'<div class="number-circle bonus">{bonus}</div>'
            tirages.append(f"<div class='numbers'>{main_circles}{bonus_circle}</div>")
        results_html = "".join(tirages)
    except ValueError:
        results_html = "Erreur : format de date invalide. Utilisez YYYYMMDD."

    content = f"""
    <div class='container'>
    <h2>Générateur de tirages</h2>
    <form method="post">
        <label>Entrez la date (YYYYMMDD) :</label>
        <input type="text" name="date_input" required value="{date_input}">
        <button type="submit" class="submit">Générer tirages</button>
    </form>
    <div class="result">{results_html}</div>
    </div>
    """
    return base_html(content)
