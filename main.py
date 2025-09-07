from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime
import random

app = FastAPI()

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

# Page principale
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Debo - Tirage de Loterie</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f2f5;
                text-align: center;
                padding: 20px;
            }
            h1 { color: #4CAF50; }
            input, button {
                padding: 12px;
                margin: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .tirage {
                background: white;
                margin: 20px auto;
                padding: 15px;
                border-radius: 10px;
                max-width: 400px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            @media (max-width: 480px) {
                .tirage { width: 90%; padding: 10px; }
                input, button { width: 90%; }
            }
        </style>
    </head>
    <body>
        <h1>Bienvenue sur Debo 🎉</h1>
        <p>Générateur de tirages de loterie française (1-90)</p>
        <form action="/tirages" method="post">
            <input type="text" name="date_input" placeholder="YYYYMMDD" required>
            <button type="submit">Générer les tirages</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Traitement du formulaire
@app.post("/tirages", response_class=HTMLResponse)
async def show_draws(date_input: str = Form(...)):
    # Vérification de la date
    try:
        datetime.strptime(date_input, "%Y%m%d")
        speed_initial = int(date_input)
    except ValueError:
        return HTMLResponse(f"<h2>Erreur : format de date invalide. Utilisez YYYYMMDD.</h2><a href='/'>Retour</a>")

    random.seed(speed_initial)
    tirages = [generate_lottery_draw(speed_initial) for _ in range(3)]

    tirages_html = ""
    for i, (mains, bonus) in enumerate(tirages):
        tirages_html += f"""
        <div class="tirage">
            <h3>Tirage {i+1}</h3>
            <p>Numéros principaux : {mains}</p>
            <p>Numéro complémentaire : {bonus}</p>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Debo - Résultats</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f2f5;
                text-align: center;
                padding: 20px;
            }}
            h1 {{ color: #4CAF50; }}
            .tirage {{
                background: white;
                margin: 20px auto;
                padding: 15px;
                border-radius: 10px;
                max-width: 400px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            @media (max-width: 480px) {{
                .tirage {{ width: 90%; padding: 10px; }}
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <h1>Résultats des tirages pour {date_input}</h1>
        {tirages_html}
        <a href="/">Retour</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
