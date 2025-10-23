from flask import Blueprint, request, jsonify
from app.db import db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.utilities.hashing import hash_password, verify_password
from app.utilities.jwt_helper import create_token

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    role = data.get("role", "patient")
    email = data.get("email")
    password = data.get("password")
    name = data.get("full_name", "")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    if role != "patient":
        return jsonify({"message": "Registration for this role is restricted"}), 403

    existing = Patient.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    new = Patient(full_name=name, email=email, password=hash_password(password))
    db.session.add(new)
    db.session.commit()

    token = create_token({"user_id": new.id, "role": "patient", "email": new.email})
    return jsonify({
        "token": token,
        "user": {"id": new.id, "email": new.email, "role": "patient"}
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = Patient.query.filter_by(email=email).first()
    role = "patient"
    if not user:
        user = Doctor.query.filter_by(email=email).first()
        role = "doctor" if user else None
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not verify_password(password, user.password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_token({"user_id": user.id, "role": role, "email": user.email})
    return jsonify({
        "token": token,
        "user": {"id": user.id, "email": user.email, "role": role}
    }), 200
