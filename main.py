from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random

app = FastAPI()

# Pour servir des fichiers CSS si nécessaire
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_lottery_draw(speed=None):
    """
    Génère un tirage :
    - 5 numéros principaux uniques (1-90)
    - 1 numéro complémentaire (1-10)
    """
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


@app.get("/", response_class=HTMLResponse)
async def form_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tirage de Loterie</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; max-width: 500px; margin: auto; }
            h1 { text-align: center; }
            form { display: flex; flex-direction: column; gap: 10px; }
            input, button { padding: 10px; font-size: 16px; }
            .result { margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>Tirage de Loterie</h1>
        <form action="/tirages" method="post">
            <label for="date_input">Date (YYYYMMDD) :</label>
            <input type="text" id="date_input" name="date_input" placeholder="20250907" required>
            <button type="submit">Générer Tirages</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/tirages", response_class=HTMLResponse)
async def generate_draw(date_input: str = Form(...)):
    try:
        datetime.strptime(date_input, "%Y%m%d")
        speed_initial = int(date_input)
    except ValueError:
        return HTMLResponse(content=f"<h2>Erreur : format de date invalide. Utilisez YYYYMMDD.</h2>")

    random.seed(speed_initial)

    tirages_html = ""
    for i in range(3):
        mains, bonus = generate_lottery_draw(speed_initial)
        tirages_html += f"<div class='result'><strong>Tirage {i+1} :</strong> Numéros principaux = {mains}, Numéro complémentaire = {bonus}</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Résultat Tirages</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 500px; margin: auto; }}
            h1 {{ text-align: center; }}
            .result {{ margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 8px; }}
            a {{ display: block; margin-top: 20px; text-align: center; text-decoration: none; color: blue; }}
        </style>
    </head>
    <body>
        <h1>Résultat des Tirages</h1>
        {tirages_html}
        <a href="/">Revenir</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
