from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, force=True)

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.services import geo_service

from app.api import cars

@asynccontextmanager
async def lifespan(app: FastAPI):
    geo_service.load_data()
    yield
    

app = FastAPI(title="CARs Map Desafio API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars.router)

@app.get("/health")
def health():
    return {"status": "ok"}
