from fastapi import APIRouter, HTTPException
import httpx

BACKEND_BASE_URL = "http://localhost:8000"
DEBUG = False

async def fetch_data(endpoint: str, params: dict = None):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"  # Ajouté '/' à la fin
    async with httpx.AsyncClient(follow_redirects=True) as client:  # Activation de follow_redirects
        print(f"Faisant requête pour: {url} avec params: {params}") if DEBUG else None
        try:
            response = await client.get(url, params=params)
            print(f"Status code: {response.status_code}") if DEBUG else None
            print(f"Réponse de {endpoint}: {response.text[:200]}...") if DEBUG else None
            
            if response.status_code == 200:
                return await response.json()
            else:
                print(f"Erreur dans la requête: Status {response.status_code}") if DEBUG else None
                return []
                
        except Exception as e:
            print(f"Erreur dans la requête pour {endpoint}: {e}") if DEBUG else None
            return []

async def create_data(endpoint: str, data: dict):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print(f"Faisant requête POST pour: {url} avec data: {data}") if DEBUG else None
        try:
            response = await client.post(url, json=data)
            print(f"Status code: {response.status_code}") if DEBUG else None
            print(f"Réponse de {endpoint}: {response.text[:200]}...") if DEBUG else None
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur dans la requête: Status {response.status_code}") if DEBUG else None
                return []
                
        except Exception as e:
            print(f"Erreur dans la requête pour {endpoint}: {e}") if DEBUG else None
            return []

async def delete_data(endpoint: str, id: str, params: dict = None):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print(f"Faisant requête DELETE pour: {url}/{id} avec id: {id}") if DEBUG else None
        try:
            response = await client.delete((url+"/"+str(id)), params=params)
            print(f"Status code: {response.status_code}") if DEBUG else None
            print(f"Réponse de {endpoint}: {response.text[:200]}...") if DEBUG else None
            
            if response.status_code == 200:
                return await {"message": "Deleted successfully"}
            else:
                print(f"Erreur dans la requête: Status {response.status_code}") if DEBUG else None
                return []
                
        except Exception as e:
            print(f"Erreur dans la requête pour {endpoint}: {e}") if DEBUG else None
            return []

async def update_data(endpoint: str, id: str, data: dict):
    url = f"{BACKEND_BASE_URL}/{endpoint}/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print(f"Faisant requête PUT pour: {url}/{id} avec data: {data}") if DEBUG else None
        try:
            response = await client.put((url+"/"+str(id)), json=data)
            print(f"Status code: {response.status_code}") if DEBUG else None
            print(f"Réponse de {endpoint}: {response.text[:200]}...") if DEBUG else None
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur dans la requête: Status {response.status_code}") if DEBUG else None
                return []
                
        except Exception as e:
            print(f"Erreur dans la requête pour {endpoint}: {e}") if DEBUG else None
            return []