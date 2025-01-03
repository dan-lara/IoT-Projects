from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from sqlite3 import Connection

from ...models.database import requestGeneric
from ...tools import get_db

router = APIRouter()

@router.post("/", response_model=dict, tags=["Generic"])
def generic_select(request: requestGeneric, db: Connection = Depends(get_db)):
    if isinstance(request.query, str) and ("SELECT" in request.query.upper()):
        if (request.params is not None) and isinstance(request.params, List):
            cursor = db.execute(request.query, request.params)
        else:
            cursor = db.execute(request.query)
    else:
        raise HTTPException(status_code=400, detail="Query must be a SELECT statement and params must be correctly provided")
    
    rows = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return {"data": jsonable_encoder(rows)}