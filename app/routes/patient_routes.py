from flask import Blueprint, jsonify, request
from app.models.patient import Patient
from app.models.record import Record
from app.db import db
from app.utilities.decorators import require_auth, require_role

patient_bp = Blueprint("patient_bp", __name__)

@patient_bp.route("/me", methods=["GET"])
@require_auth
@require_role("patient")
def me():
    user = request.user
    p = Patient.query.get(user["user_id"])
    if not p:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": p.id,
        "full_name": p.full_name,
        "email": p.email,
        "phone": p.phone,
        "condition": p.condition
    })

@patient_bp.route("/records", methods=["GET"])
@require_auth
@require_role("patient")
def my_records():
    user = request.user
    records = Record.query.filter_by(patient_id=user["user_id"]).all()
    out = []
    for r in records:
        out.append({
            "id": r.id,
            "diagnosis": r.diagnosis,
            "prescription": r.prescription,
            "date_of_visit": r.date_of_visit.isoformat() if r.date_of_visit else None,
            "doctor": {"id": r.doctor.id, "full_name": r.doctor.full_name} if r.doctor else None
        })
    return jsonify(out)
