from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import calc_superavit
import os

directory = "./static"
if not os.path.exists(directory):
    os.makedirs(directory)

class Ecuations(BaseModel):
    demand: str
    offer: str

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calc/")
async def calc(ecuations: Ecuations):
    try:
        filename = "static/graph.png"
        superavit = calc_superavit.superavit(ecuations.demand, ecuations.offer, filename)
        return { "superavit": superavit, "image_url": f"https://old-erica-simon-j-bbe8e266.koyeb.app/{filename}" }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Servir archivos estáticos
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
