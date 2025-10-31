from flask import Blueprint, request, jsonify
from app.db import get_db_connection, release_db_connection
from app.utilities.jwt_helper import create_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_patient():
    data = request.get_json()

    required_fields = ["full_name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM patients WHERE email = %s", (data["email"],))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 400

        hashed_password = generate_password_hash(data["password"])

        # Insert patient
        patient_data = (
            data["full_name"],
            data["email"],
            data.get("phone"),
            hashed_password,
            data.get("date_of_birth"),
            data.get("first_aid_procedure"),
            data.get("allergies"),
            data.get("next_of_kin_name"),
            data.get("next_of_kin_phone"),
            data.get("caregiver_name"),
            data.get("caregiver_phone"),
        )
        cursor.execute("""
            INSERT INTO patients (full_name, email, phone, password, date_of_birth, first_aid_procedure, allergies, next_of_kin_name, next_of_kin_phone, caregiver_name, caregiver_phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, patient_data)
        new_patient_id = cursor.fetchone()["id"]

        # Create emergency profile
        cursor.execute("INSERT INTO emergency_profiles (patient_id, public_id, public_visible) VALUES (%s, %s, %s)", (new_patient_id, f"EP{new_patient_id:06d}", False))

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        release_db_connection(conn)

    return jsonify({"message": "Patient registered successfully"}), 201

# login
@auth_bp.route("/login", methods=["POST"])
def login_patient():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM patients WHERE email = %s", (data.get("email"),))
        patient = cursor.fetchone()

        if not patient or not check_password_hash(patient["password"], data.get("password")):
            return jsonify({"error": "Invalid email or password"}), 401

        token = create_token({"patient_id": patient["id"]})
        return jsonify({
            "token": token,
            "patient_id": patient["id"],
            "full_name": patient["full_name"]
        }), 200
    finally:
        cursor.close()
        release_db_connection(conn)
