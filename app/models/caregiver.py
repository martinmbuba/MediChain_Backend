from app.db import db
from datetime import datetime

class Caregiver(db.Model):
    __tablename__ = "caregivers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    relation = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
