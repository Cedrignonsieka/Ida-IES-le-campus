from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import random
from datetime import datetime

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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Loterie</title>
<style>
body {{ font-family: Arial, sans-serif; padding: 0; margin:0; background: #f0f2f5; }}
header {{ background: #007bff; color: white; padding: 15px; display: flex; justify-content: space-around; }}
header a {{ color: white; text-decoration: none; font-weight: bold; }}
header a:hover {{ text-decoration: underline; }}
footer {{ background: #333; color: white; text-align: center; padding: 10px; position: fixed; width: 100%; bottom: 0; }}
.container {{ max-width: 400px; margin: 80px auto 60px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
input[type="text"] {{ width: 100%; padding: 8px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; }}
button {{ width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }}
button:hover {{ background: #218838; }}
.result {{ margin-top: 20px; }}
.numbers {{ display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; opacity: 0; animation: fadeIn 0.5s forwards; }}
.number-circle {{ width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #007bff; color: white; font-weight: bold; transition: transform 0.3s; }}
.number-circle:hover {{ transform: scale(1.2); }}
.bonus {{ background: #dc3545 !important; }}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(-10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
</head>
<body>
<header>
    <a href="/">ACCUEIL</a>
    <a href="/">VÉRIFIER</a>
</header>
<div class="container">
<h2>Générateur de tirages</h2>
<form method="post">
<label>Entrez la date (YYYYMMDD) :</label>
<input type="text" name="date_input" required>
<button type="submit">Générer tirages</button>
</form>
<div class="result">
{results}
</div>
</div>
<footer>
    &copy; 2025 Mon site Loterie. Tous droits réservés.
</footer>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def home(date_input: str = Form(None)):
    results_html = ""
    if date_input:
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
    return HTML_TEMPLATE.format(results=results_html)
