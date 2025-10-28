from app.db import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(255))
    condition = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # New medical & emergency info
    first_aid_procedure = db.Column(db.Text)
    allergies = db.Column(db.Text)
    next_of_kin_name = db.Column(db.String(255))
    next_of_kin_phone = db.Column(db.String(50))
    caregiver_name = db.Column(db.String(255))
    caregiver_phone = db.Column(db.String(50))

    
    records = db.relationship("Record", backref="patient", lazy="dynamic")
    caregivers = db.relationship("Caregiver", backref="patient", lazy="dynamic")
    reminders = db.relationship("Reminder", backref="patient", lazy="dynamic")
    emergency_profile = db.relationship("EmergencyProfile", backref="patient", uselist=False)
