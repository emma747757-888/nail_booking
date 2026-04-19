from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import sqlite3

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================
# STATIC FILES
# =====================
app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================
# JINJA TEMPLATE SETUP
# =====================
templates = Jinja2Templates(directory="templates")


# =====================
# PAGES
# =====================
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })


@app.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {
        "request": request
    })


# =====================
# CALENDAR API
# =====================
@app.get("/api/calendar")
def calendar():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "nail_booking.db"))
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, c.name, s.name, a.date, a.time
        FROM appointments a
        JOIN customers c ON a.customer_id = c.id
        JOIN services s ON a.service_id = s.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": f"{r[1]} - {r[2]}",
            "start": f"{r[3]}T{r[4]}"
        }
        for r in rows
    ]
