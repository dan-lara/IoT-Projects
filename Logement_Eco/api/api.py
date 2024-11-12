from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Rota principal para testar a renderização do template com gráfico
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    # Dados simulados para enviar ao template
    data = {
        "sensor": "Temperature",
        "value": f"{random.randint(20, 30)}°C",  # Gera um valor aleatório para simular a temperatura
        "status": "Active",
        "consumption": [
            ["Eau", random.randint(20, 50)],
            ["Eléctricite", random.randint(30, 60)],
            ["Déchets", random.randint(10, 30)]
        ]
    }
    return templates.TemplateResponse("home.html", {"request": request, "data": data})
