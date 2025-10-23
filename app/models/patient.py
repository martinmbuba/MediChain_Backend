from app.db import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    condition = db.Column(db.Text)
    password = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship("Record", backref="patient", lazy="dynamic")
    caregivers = db.relationship("Caregiver", backref="patient", lazy="dynamic")
    reminders = db.relationship("Reminder", backref="patient", lazy="dynamic")
    emergency_profile = db.relationship("EmergencyProfile", backref="patient", uselist=False)
