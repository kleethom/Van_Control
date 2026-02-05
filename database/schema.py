from database.db import get_db

def init_schema():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS system_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_ts INTEGER NOT NULL,
        end_ts INTEGER
    );

    CREATE TABLE IF NOT EXISTS sensor_raw (
        timestamp INTEGER PRIMARY KEY,
        temperature_inside REAL,
        humidity_inside REAL,
        temperature_outside REAL,
        humidity_outside REAL,
        pressure REAL,
        altitude REAL,
        tilt_x REAL,
        tilt_y REAL
    );

    CREATE TABLE IF NOT EXISTS sensor_1min (
        timestamp INTEGER PRIMARY KEY,
        temp_in_avg REAL,
        temp_in_min REAL,
        temp_in_max REAL,
        hum_in_avg REAL,
        temp_out_avg REAL,
        temp_out_min REAL,
        temp_out_max REAL,
        hum_out_avg REAL,
        altitude_avg REAL
    );

    CREATE TABLE IF NOT EXISTS sensor_1hour (
        timestamp INTEGER PRIMARY KEY,
        temp_in_avg REAL,
        temp_in_min REAL,
        temp_in_max REAL,
        hum_in_avg REAL,
        temp_out_avg REAL,
        temp_out_min REAL,
        temp_out_max REAL,
        hum_out_avg REAL,
        altitude_avg REAL
    );

    CREATE TABLE IF NOT EXISTS sensor_1day (
        date INTEGER PRIMARY KEY,
        temp_in_avg REAL,
        temp_in_min REAL,
        temp_in_max REAL,
        hum_in_avg REAL,
        temp_out_avg REAL,
        temp_out_min REAL,
        temp_out_max REAL,
        hum_out_avg REAL,
        altitude_avg REAL
    );
    """)
    db.commit()