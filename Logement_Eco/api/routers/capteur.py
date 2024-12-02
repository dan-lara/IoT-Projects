from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
router = APIRouter()

BACKEND_BASE_URL = "http://localhost:8000/capteur/"  # Remplacez par l'URL correcte de l'API backend

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=["Capteur"])
async def get_capteurs_page(request: Request, id_tc: int = None, id_p: int = None):
    capteurs = None
    if id_tc or id_p:
        # Faire la requête pour le backend des capteurs
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BACKEND_BASE_URL,
                    params={"id_tc": id_tc, "id_p": id_p}
                )
            if response.status_code == 200:
                capteurs = response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching capteurs data.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")

    # Rendre la page avec les données ou sans données si les filtres ne sont pas fournis
    return templates.TemplateResponse("capteurs.html", {"request": request, "capteurs": capteurs})