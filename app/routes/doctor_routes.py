from flask import Blueprint, request, jsonify
from app.models.doctor import Doctor
from app.models.record import Record
from app.db import db
from app.utilities.decorators import require_auth, require_role
from app.models.patient import Patient

doctor_bp = Blueprint("doctor_bp", __name__)

@doctor_bp.route("/patients", methods=["GET"])
@require_auth
@require_role("doctor")
def patients_list():
    ps = Patient.query.all()
    return jsonify([
        {"id": p.id, "full_name": p.full_name, "email": p.email}
        for p in ps
    ])

@doctor_bp.route("/record", methods=["POST"])
@require_auth
@require_role("doctor")
def add_record():
    data = request.get_json()
    doctor_id = request.user["user_id"]
    patient_id = data.get("patient_id")
    diagnosis = data.get("diagnosis")
    prescription = data.get("prescription")

    rec = Record(
        patient_id=patient_id,
        doctor_id=doctor_id,
        diagnosis=diagnosis,
        prescription=prescription
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify({"message": "record added", "id": rec.id}), 201
