import uuid
from datetime import datetime
from app.db import db

def gen_public_id():
    return uuid.uuid4().hex

class EmergencyProfile(db.Model):
    __tablename__ = "emergency_profiles"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), unique=True, nullable=False)
    public_id = db.Column(db.String(32), unique=True, nullable=False, default=gen_public_id)
    public_visible = db.Column(db.Boolean, default=False, nullable=False)
    public_phone_visible = db.Column(db.Boolean, default=False, nullable=False)
    qr_token = db.Column(db.String(255), unique=True, nullable=True)
    visible_fields = db.Column(db.JSON, default={})
    blood_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_public_dict(self):
        """Public view of the profile including patient’s shared info"""
        if not self.public_visible:
            return None

        patient = self.patient  
        return {
            "full_name": patient.full_name,
            "phone": patient.phone if self.public_phone_visible else None,
            "allergies": patient.allergies,
            "first_aid_procedure": patient.first_aid_procedure,
            "next_of_kin_name": patient.next_of_kin_name,
            "next_of_kin_phone": patient.next_of_kin_phone,
            "caregiver_name": patient.caregiver_name,
            "caregiver_phone": patient.caregiver_phone,
            "blood_type": self.blood_type,
            "visible_fields": self.visible_fields,
        }
