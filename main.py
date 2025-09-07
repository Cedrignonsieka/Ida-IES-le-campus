from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import random

app = FastAPI()

# Route pour servir les fichiers statiques (CSS si besoin)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Page d'accueil avec formulaire
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Debo - Générateur de tirages</title>
            <style>
                body { font-family: Arial; text-align:center; margin-top:50px; }
                input, button { font-size: 16px; padding: 8px; margin:5px; }
            </style>
        </head>
        <body>
            <h1>Bienvenue sur Debo 🎉</h1>
            <form action="/generate" method="post">
                <label>Entrez une date (YYYY-MM-DD) :</label><br>
                <input type="text" name="date_str" required>
                <button type="submit">Générer</button>
            </form>
        </body>
    </html>
    """

# Route pour générer les tirages depuis le formulaire
@app.post("/generate", response_class=HTMLResponse)
def generate(date_str: str = Form(...)):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return f"<h2>Format de date invalide : {date_str}</h2><a href='/'>Retour</a>"

    blocs = []
    for _ in range(3):
        bloc = random.sample(range(1, 91), 5)
        blocs.append(bloc)

    # Générer le HTML de sortie
    bloc_html = "".join(
        [f"<p>Bloc {i+1}: {', '.join(map(str, bloc))}</p>" for i, bloc in enumerate(blocs)]
    )

    return f"""
    <html>
        <head>
            <title>Tirages pour {date_str}</title>
        </head>
        <body style='text-align:center; font-family:Arial; margin-top:50px;'>
            <h1>Tirages pour {date_str}</h1>
            {bloc_html}
            <a href="/">Retour</a>
        </body>
    </html>
    """
