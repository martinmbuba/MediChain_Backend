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
    allergies = db.Column(db.Text)
    next_of_kin_name = db.Column(db.String(255))
    next_of_kin_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_public_dict(self):
        """
        Returns a sanitized version of the profile for public access
        """
        if not self.public_visible:
            return None

        data = {
            "blood_type": self.blood_type,
            "allergies": self.allergies,
            "next_of_kin_name": self.next_of_kin_name,
            "next_of_kin_phone": self.next_of_kin_phone if self.public_phone_visible else None,
            "visible_fields": self.visible_fields,
        }
        return data
