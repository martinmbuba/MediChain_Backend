from flask import Blueprint, request, jsonify
from app.models.patient import Patient
from app.db import db
from app.utilities.decorators import token_required

patient_bp = Blueprint("patient_bp", __name__)

#VIEW PROFILE 
@patient_bp.route("/patient/profile", methods=["GET"])
@token_required
def view_profile(current_user):
    # current_user should already be a Patient instance
    patient = Patient.query.get(current_user.id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify({
        "id": patient.id,
        "full_name": patient.full_name,
        "email": patient.email,
        "phone": patient.phone,
        "date_of_birth": str(patient.date_of_birth) if patient.date_of_birth else None,
        "first_aid_procedure": patient.first_aid_procedure,
        "allergies": patient.allergies,
        "next_of_kin_name": patient.next_of_kin_name,
        "next_of_kin_phone": patient.next_of_kin_phone,
        "caregiver_name": patient.caregiver_name,
        "caregiver_phone": patient.caregiver_phone
    }), 200


#  UPDATE PROFILE 
@patient_bp.route("/patient/update", methods=["PATCH"])
@token_required
def update_profile(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    patient = Patient.query.get(current_user.id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    protected_fields = ["id", "email", "password"]
    for field, value in data.items():
        if field not in protected_fields and hasattr(patient, field):
            setattr(patient, field, value)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
