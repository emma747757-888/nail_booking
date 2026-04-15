import sqlite3

conn = sqlite3.connect("nail_booking.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    visit_count INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    date TEXT,
    time TEXT,
    service TEXT,
    status TEXT,
    rating TEXT,
    comment TEXT,
    visit_count INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("DB ready")
