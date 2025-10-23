from app.db import db
from datetime import datetime

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    file_url = db.Column(db.Text)
    date_of_visit = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
