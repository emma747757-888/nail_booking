import sqlite3

conn = sqlite3.connect("nail_booking.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    duration INTEGER
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    staff_id INTEGER,
    service_id INTEGER,
    date TEXT,
    time TEXT,
    status TEXT DEFAULT 'scheduled'
);
""")

conn.commit()
conn.close()

print("DB initialized ✔")