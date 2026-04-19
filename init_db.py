import sqlite3

conn = sqlite3.connect("nail_booking.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    service_id INTEGER,
    date TEXT,
    time TEXT
);
""")

conn.commit()
conn.close()
print("DB ready ✔")