from app.db import db

class EmergencyProfile(db.Model):
    __tablename__ = "emergency_profiles"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), unique=True, nullable=False)
    qr_token = db.Column(db.String(255))
    visible_fields = db.Column(db.JSON)
    blood_type = db.Column(db.String(20))
    allergies = db.Column(db.Text)
    next_of_kin_name = db.Column(db.String(255))
    next_of_kin_phone = db.Column(db.String(50))
