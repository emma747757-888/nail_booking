from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# =========================
# ADMIN
# =========================
@app.get("/admin", response_class=HTMLResponse)
def admin():
    with open(os.path.join(BASE_DIR, "admin.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
