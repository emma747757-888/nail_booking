from fastapi import FastAPI
import sqlite3
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# =========================
# 静态文件
# =========================
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HTML PATH（关键修复）
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# MODELS
# =========================
class AppointmentRequest(BaseModel):
    name: str
    phone: str
    service: str
    date: str
    time: str

class ReviewRequest(BaseModel):
    rating: int
    comment: str

class StatusRequest(BaseModel):
    status: str

# =========================
# DATABASE
# =========================
def get_conn():
    return sqlite3.connect("nail_booking.db")

# =========================
# HOME PAGE
# =========================
@app.get("/")
def home():
    with open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8") as f:
        return f.read()

# =========================
# ADMIN PAGE
# =========================
@app.get("/admin")
def admin():
    with open(os.path.join(BASE_DIR, "admin.html"), encoding="utf-8") as f:
        return f.read()

# =========================
# APPOINTMENTS
# =========================
@app.get("/appointments/")
def list_appointments():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, c.name, c.phone, a.service, a.date, a.time, a.status, a.staff_id
        FROM appointments a
        JOIN customers c ON a.customer_id = c.id
        ORDER BY a.date ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "phone": r[2],
            "service": r[3],
            "date": r[4],
            "time": r[5],
            "status": r[6],
            "staff_id": r[7]
        }
        for r in rows
    ]

# =========================
# SERVICES
# =========================
@app.get("/services/")
def get_services():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, duration FROM services")
    rows = cursor.fetchall()

    conn.close()

    return [{"id": r[0], "name": r[1], "duration": r[2]} for r in rows]

# =========================
# STAFF
# =========================
@app.get("/staff/")
def get_staff():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM staff")
    rows = cursor.fetchall()

    conn.close()

    return [{"id": r[0], "name": r[1]} for r in rows]

# =========================
# RESCHEDULE
# =========================
@app.put("/appointments/{appointment_id}/reschedule")
def reschedule(appointment_id: int, data: dict):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE appointments
        SET date=?, time=?, staff_id=?
        WHERE id=?
    """, (
        data["date"],
        data["time"],
        data["staff_id"],
        appointment_id
    ))

    conn.commit()
    conn.close()

    return {"message": "rescheduled"}
