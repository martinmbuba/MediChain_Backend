from app.db import db
from datetime import datetime

class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    description = db.Column(db.Text)
    reminder_type = db.Column(db.String(100))
    scheduled_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
