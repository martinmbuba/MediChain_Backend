from flask import Blueprint, request, jsonify, g
from app.db import db
from app.models.patient import Patient
from app.models.record import Record
from app.utilities.decorators import require_auth, require_role

doctor_bp = Blueprint("doctor_bp", __name__)

# ---------------------------------------------------
# 1. Search Patient by Email
# ---------------------------------------------------
@doctor_bp.route("/patient/search", methods=["GET"])
@require_auth
@require_role("doctor")
def search_patient():
    email = request.args.get("email")
    if not email:
        return jsonify({"message": "Email query required: /patient/search?email=..."}), 400

    patient = Patient.query.filter_by(email=email).first()
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    return jsonify({
        "id": patient.id,
        "full_name": patient.full_name,
        "email": patient.email,
        "phone": patient.phone,
        "condition": patient.condition
    }), 200


# ---------------------------------------------------
# 2. View Patient Medical Records
# ---------------------------------------------------
@doctor_bp.route("/patient/<int:patient_id>/records", methods=["GET"])
@require_auth
@require_role("doctor")
def view_records(patient_id):
    records = Record.query.filter_by(patient_id=patient_id).all()

    if not records:
        return jsonify({"message": "No records found for this patient"}), 404

    output = []
    for r in records:
        output.append({
            "id": r.id,
            "doctor_id": r.doctor_id,
            "diagnosis": r.diagnosis,
            "prescription": r.prescription,
            "file_url": r.file_url,
            "date_of_visit": r.date_of_visit,
            "created_at": r.created_at
        })

    return jsonify({"records": output}), 200


# ---------------------------------------------------
# 3. Add New Medical Record
# ---------------------------------------------------
@doctor_bp.route("/patient/<int:patient_id>/records", methods=["POST"])
@require_auth
@require_role("doctor")
def add_record(patient_id):
    data = request.get_json()

    diagnosis = data.get("diagnosis")
    if not diagnosis:
        return jsonify({"message": "Diagnosis is required"}), 400

    prescription = data.get("prescription")
    file_url = data.get("file_url")
    date_of_visit = data.get("date_of_visit")

    new_record = Record(
        patient_id=patient_id,
        doctor_id=g.user["user_id"],   # doctor id from token
        diagnosis=diagnosis,
        prescription=prescription,
        file_url=file_url,
        date_of_visit=date_of_visit
    )

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "Record added successfully"}), 201
