from flask import Blueprint, request, jsonify
from app.models.patient import Patient
from app.models.emergency_profile import EmergencyProfile
from app.db import db
from app.utilities.jwt_helper import create_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__)
@auth_bp.route("/register", methods=["POST"])
def register_patient():
    data = request.get_json()

    required_fields = ["full_name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if Patient.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data["password"])

    new_patient = Patient(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        password=hashed_password,
        date_of_birth=data.get("date_of_birth"),
        first_aid_procedure=data.get("first_aid_procedure"),
        allergies=data.get("allergies"),
        next_of_kin_name=data.get("next_of_kin_name"),
        next_of_kin_phone=data.get("next_of_kin_phone"),
        caregiver_name=data.get("caregiver_name"),
        caregiver_phone=data.get("caregiver_phone"),
    )

    db.session.add(new_patient)
    db.session.commit()

    emergency_profile = EmergencyProfile(patient_id=new_patient.id)
    db.session.add(emergency_profile)
    db.session.commit()

    return jsonify({"message": "Patient registered successfully"}), 201


# login
@auth_bp.route("/login", methods=["POST"])
def login_patient():
    data = request.get_json()

    patient = Patient.query.filter_by(email=data.get("email")).first()
    if not patient or not check_password_hash(patient.password, data.get("password")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_token({"patient_id": patient.id})
    return jsonify({
        "token": token,
        "patient_id": patient.id,
        "full_name": patient.full_name
    }), 200
