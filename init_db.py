import sqlite3

conn = sqlite3.connect("nail_booking.db")
cursor = conn.cursor()

# =====================
# services
# =====================
cursor.execute("""
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    duration INTEGER
)
""")

# =====================
# customers
# =====================
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    visit_count INTEGER
)
""")

# =====================
# appointments
# =====================
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    service TEXT,
    date TEXT,
    time TEXT,
    status TEXT
)
""")

# =====================
# seed data（可重复运行）
# =====================
cursor.executemany("""
INSERT INTO services (name, duration)
SELECT ?, ?
WHERE NOT EXISTS (
    SELECT 1 FROM services WHERE name=?
)
""", [
    ("BIAB", 60, "BIAB"),
    ("Gel", 45, "Gel"),
    ("Nail Art", 90, "Nail Art")
])

conn.commit()
conn.close()

print("Database ready ✔")
