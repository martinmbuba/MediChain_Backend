from flask import Blueprint, jsonify
from app.db import get_db_connection

emergency_bp = Blueprint("emergency_bp", __name__)

# PUBLIC EMERGENCY VIEW
@emergency_bp.route("/<string:patient_id>", methods=["GET"])
def public_emergency_view(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # Get emergency profile
        cursor.execute("SELECT * FROM emergency_profiles WHERE patient_id = %s", (patient_id,))
        profile = cursor.fetchone()

        if not profile or not profile["public_visible"]:
            return jsonify({"error": "Profile not accessible"}), 403

        # Get patient data
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify({
            "full_name": patient["full_name"],
            "phone": patient["phone"] if profile.get("public_phone_visible", False) else None,
            "allergies": patient["allergies"],
            "first_aid_procedure": patient["first_aid_procedure"],
            "next_of_kin_name": patient["next_of_kin_name"],
            "next_of_kin_phone": patient["next_of_kin_phone"],
            "caregiver_name": patient["caregiver_name"],
            "caregiver_phone": patient["caregiver_phone"],
            "blood_type": profile.get("blood_type"),
            "visible_fields": profile.get("visible_fields", {})
        }), 200
    finally:
        cursor.close()
        conn.close()
