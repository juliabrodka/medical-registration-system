PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS patients
(
    patient_id INTEGER PRIMARY KEY,
    first_name TEXT    NOT NULL,
    last_name  TEXT    NOT NULL,
    pesel      TEXT    NOT NULL UNIQUE,
    phone      TEXT,
    email      TEXT,
    address    TEXT,
    active     INTEGER NOT NULL DEFAULT 1,

    CHECK (active IN (0, 1)),
    CHECK (
        (phone IS NOT NULL AND TRIM(phone) <> '')
            OR
        (email IS NOT NULL AND TRIM(email) <> '')
        )
);
CREATE TABLE IF NOT EXISTS doctors
(
    doctor_id       INTEGER PRIMARY KEY,
    employee_number TEXT    NOT NULL UNIQUE,
    first_name      TEXT    NOT NULL,
    last_name       TEXT    NOT NULL,
    specialization  TEXT    NOT NULL,
    room            TEXT,
    active          INTEGER NOT NULL DEFAULT 1,
    CHECK ( active IN (0, 1) )

);
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY,

    date TEXT NOT NULL,
    time TEXT NOT NULL,

    doctor_id INTEGER NOT NULL,
    patient_id INTEGER,

    status TEXT NOT NULL DEFAULT 'FREE',

    FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    UNIQUE (doctor_id, date, time),

    CHECK (status IN ('FREE', 'BOOKED', 'CANCELLED')),

    CHECK (
        (status = 'FREE' AND patient_id IS NULL)
        OR (status = 'BOOKED' AND patient_id IS NOT NULL)
        OR status = 'CANCELLED'
    )
);

CREATE INDEX IF NOT EXISTS idx_patients_last_name
ON patients(last_name);

CREATE INDEX IF NOT EXISTS idx_doctors_last_name
ON doctors(last_name);

CREATE INDEX IF NOT EXISTS idx_doctors_specialization
ON doctors(specialization);

CREATE INDEX IF NOT EXISTS idx_appointments_patient_id
ON appointments(patient_id);

CREATE INDEX IF NOT EXISTS idx_appointments_doctor_status_date
ON appointments(doctor_id, status, date);

CREATE INDEX IF NOT EXISTS idx_doctor_status_date
ON appointments(doctor_id,status,date);