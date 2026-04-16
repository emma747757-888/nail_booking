from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles  

app = FastAPI()

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# CORS
# =========================
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
# DATABASE HELPERS
# =========================
def get_conn():
    return sqlite3.connect("nail_booking.db")


# =========================
# SLOT LOGIC
# =========================
def is_slot_taken(date, time):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM appointments
        WHERE date=? AND time=?
    """, (date, time))

    result = cursor.fetchone()
    conn.close()

    return result is not None


def generate_slots(start="10:00", end="19:00", step=30):
    slots = []
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")

    while current < end_time:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=step)

    return slots


def get_booked_slots(date):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT time FROM appointments WHERE date=?
    """, (date,))

    booked = [row[0] for row in cursor.fetchall()]
    conn.close()

    return booked


# =========================
# STAFF AUTO ASSIGN
# =========================
def find_best_staff(date, time):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM staff")
    staff_list = cursor.fetchall()

    best_staff = None
    min_load = float("inf")

    new_start = datetime.strptime(time, "%H:%M")
    new_end = new_start + timedelta(minutes=30)

    for (staff_id,) in staff_list:

        cursor.execute("""
            SELECT time FROM appointments
            WHERE date=? AND staff_id=?
        """, (date, staff_id))

        bookings = cursor.fetchall()
        load = len(bookings)

        conflict = False

        for (t,) in bookings:
            exist_start = datetime.strptime(t, "%H:%M")
            exist_end = exist_start + timedelta(minutes=30)

            if not (new_end <= exist_start or new_start >= exist_end):
                conflict = True
                break

        if not conflict and load < min_load:
            min_load = load
            best_staff = staff_id

    conn.close()
    return best_staff


# =========================
# CREATE APPOINTMENT
# =========================
@app.post("/appointments/")
def create_appointment(data: AppointmentRequest):
    conn = get_conn()
    cursor = conn.cursor()

    if is_slot_taken(data.date, data.time):
        return {"error": "This slot is already booked ❌"}

    # customer
    cursor.execute("SELECT id, visit_count FROM customers WHERE phone=?", (data.phone,))
    customer = cursor.fetchone()

    if customer:
        customer_id, visit_count = customer
        visit_count += 1
        cursor.execute(
            "UPDATE customers SET visit_count=? WHERE id=?",
            (visit_count, customer_id)
        )
    else:
        cursor.execute(
            "INSERT INTO customers (name, phone, visit_count) VALUES (?,?,?)",
            (data.name, data.phone, 1)
        )
        customer_id = cursor.lastrowid

    # staff auto assign
    staff_id = find_best_staff(data.date, data.time)

    # insert appointment
    cursor.execute("""
        INSERT INTO appointments (customer_id, service, date, time, staff_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, data.service, data.date, data.time, staff_id, "scheduled"))

    conn.commit()
    conn.close()

    return {"message": "created"}


# =========================
# GET APPOINTMENTS
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

    return [
        {"id": r[0], "name": r[1], "duration": r[2]}
        for r in rows
    ]


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

    return [
        {"id": r[0], "name": r[1]}
        for r in rows
    ]


# =========================
# AVAILABILITY
# =========================
@app.get("/availability/")
def get_availability(date: str):
    all_slots = generate_slots()
    booked = get_booked_slots(date)

    return {
        "date": date,
        "available_slots": [s for s in all_slots if s not in booked]
    }


# =========================
# STATUS UPDATE
# =========================
@app.put("/appointments/{appointment_id}/status")
def update_status(appointment_id: int, data: StatusRequest):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE appointments SET status=?
        WHERE id=?
    """, (data.status, appointment_id))

    conn.commit()
    conn.close()

    return {"message": "updated"}


# =========================
# REVIEW
# =========================
@app.put("/appointments/{appointment_id}/review")
def add_review(appointment_id: int, data: ReviewRequest):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE appointments
        SET rating=?, comment=?
        WHERE id=?
    """, (data.rating, data.comment, appointment_id))

    conn.commit()
    conn.close()

    return {"message": "review added"}


# =========================
# RESCHEDULE (DRAG & DROP)
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

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/admin", response_class=HTMLResponse)
def admin():
    with open("admin.html", "r", encoding="utf-8") as f:
        return f.read()
