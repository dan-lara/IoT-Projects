from fastapi import APIRouter, HTTPException

from models.database import Ville

router = APIRouter()

# Route pour récupérer toutes les villes
@router.get("/", response_model=list[Ville])
async def read_villes():
    return await Ville.objects.prefetch_related("adresses").all()