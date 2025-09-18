from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import random
from datetime import datetime

app = FastAPI()

# Votre code de génération de tirage...
def generate_lottery_draw(speed=None):
    # ... (le code que vous avez déjà)
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

# Votre code HTML...
HOME_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accueil - Loterie</title>
    <style>
    body { font-family: Arial, sans-serif; padding: 0; margin:0; background: #f0f2f5; }
    header { background: #007bff; color: white; padding: 15px; display: flex; justify-content: space-around; }
    header a { color: white; text-decoration: none; font-weight: bold; }
    header a:hover { text-decoration: underline; }
    footer { background: #333; color: white; text-align: center; padding: 10px; position: fixed; width: 100%; bottom: 0; }
    .container { max-width: 600px; margin: 80px auto 60px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }
    .quote { font-size: 1.5em; font-style: italic; color: #555; margin-bottom: 20px; }
    .author { font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <header>
        <a href="/">ACCUEIL</a>
        <a href="/verifier">VÉRIFIER</a>
    </header>
    <div class="container">
        <p class="quote">« Il est dur d'échouer ; mais il est pire de n'avoir jamais tenté de réussir. »</p>
        <p class="author">- Franklin Roosevelt</p>
    </div>
    <footer>
        &copy; 2025 Mon site Loterie. Tous droits réservés.
    </footer>
</body>
</html>
"""

VERIFIER_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Loterie</title>
<style>
body { font-family: Arial, sans-serif; padding: 0; margin:0; background: #f0f2f5; }
header { background: #007bff; color: white; padding: 15px; display: flex; justify-content: space-around; }
header a { color: white; text-decoration: none; font-weight: bold; }
header a:hover { text-decoration: underline; }
footer { background: #333; color: white; text-align: center; padding: 10px; position: fixed; width: 100%; bottom: 0; }
.container { max-width: 400px; margin: 80px auto 60px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
input[type="text"] { width: 100%; padding: 8px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; }
button { width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
button:hover { background: #218838; }
.result { margin-top: 20px; }
.numbers { display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; opacity: 0; animation: fadeIn 0.5s forwards; }
.number-circle { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background
"""

# AJOUT DES ROUTES
@app.get("/", response_class=HTMLResponse)
async def home():
    """Route pour la page d'accueil."""
    return HOME_HTML

@app.get("/verifier", response_class=HTMLResponse)
async def verifier():
    """Route pour la page de vérification."""
    return VERIFIER_HTML_TEMPLATE
