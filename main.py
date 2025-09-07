from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
from datetime import datetime

app = FastAPI()

# Dossiers pour fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/verifier", response_class=HTMLResponse)
async def verifier(request: Request):
    return templates.TemplateResponse("verifier.html", {"request": request, "results": ""})


@app.post("/verifier", response_class=HTMLResponse)
async def verifier_post(request: Request, date_input: str = Form(...)):
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

    return templates.TemplateResponse("verifier.html", {"request": request, "results": results_html})
