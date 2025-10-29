from flask import Blueprint, request, jsonify
from app.models.caregiver import Caregiver
from app.models.patient import Patient
from app.models.record import Record
from app.utilities.decorators import token_required
from app.db import db

caregiver_bp = Blueprint("caregiver_bp", __name__)


@caregiver_bp.route("/register", methods=["POST"])  
def register_caregiver():
    data = request.get_json()
    patient_id = data.get("patient_id")

    if not patient_id or not Patient.query.get(patient_id):
        return jsonify({"error": "Patient not found"}), 404

    caregiver = Caregiver(
        full_name=data["full_name"],
        phone=data.get("phone"),
        email=data.get("email"),
        relation=data.get("relation"),
        patient_id=patient_id
    )
    db.session.add(caregiver)
    db.session.commit()

    return jsonify({"message": "Caregiver registered successfully"}), 201

#  VIEW PATIENT RECORDS 
@caregiver_bp.route("/<int:patient_id>/records", methods=["GET"])  # ✅ removed /caregiver prefix
def caregiver_view_patient_records(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    records = Record.query.filter_by(patient_id=patient_id).all()
    return jsonify([
        {
            "id": record.id,
            "description": record.description,
            "created_at": str(record.created_at)
        } for record in records
    ]), 200
