-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    password VARCHAR(255),
    condition TEXT,
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first_aid_procedure TEXT,
    allergies TEXT,
    next_of_kin_name VARCHAR(255),
    next_of_kin_phone VARCHAR(50),
    caregiver_name VARCHAR(255),
    caregiver_phone VARCHAR(50)
);

-- Create caregivers table
CREATE TABLE IF NOT EXISTS caregivers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255) UNIQUE,
    relation VARCHAR(255),
    password VARCHAR(255),
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create emergency_profiles table
CREATE TABLE IF NOT EXISTS emergency_profiles (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER UNIQUE NOT NULL REFERENCES patients(id),
    public_id VARCHAR(32) UNIQUE NOT NULL,
    public_visible BOOLEAN NOT NULL DEFAULT FALSE,
    public_phone_visible BOOLEAN NOT NULL DEFAULT FALSE,
    qr_token VARCHAR(255) UNIQUE,
    visible_fields JSONB DEFAULT '{}',
    blood_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create records table
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    diagnosis TEXT,
    prescription TEXT,
    file_url TEXT,
    date_of_visit DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    medication VARCHAR(255) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    duration VARCHAR(100),
    prescribed_by VARCHAR(255),
    date DATE,
    notes TEXT,
    completed BOOLEAN DEFAULT FALSE,
    taken_doses INTEGER DEFAULT 0,
    total_doses INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    caregiver_id INTEGER REFERENCES caregivers(id),
    description TEXT,
    reminder_type VARCHAR(100),
    scheduled_time TIMESTAMP,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
