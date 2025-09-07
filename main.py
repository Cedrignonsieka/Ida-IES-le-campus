from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
from datetime import datetime

app = FastAPI()
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
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tirages": None})

@app.post("/tirages", response_class=HTMLResponse)
def tirages(request: Request, date_input: str = Form(...)):
    try:
        datetime.strptime(date_input, "%Y%m%d")
        speed_initial = int(date_input)
    except ValueError:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "tirages": None, "error": "Format de date invalide. Utilisez YYYYMMDD."}
        )
    random.seed(speed_initial)
    results = []
    for _ in range(3):
        mains, bonus = generate_lottery_draw(speed_initial)
        results.append({"main": mains, "bonus": bonus})
    return templates.TemplateResponse("index.html", {"request": request, "tirages": results, "error": None})
