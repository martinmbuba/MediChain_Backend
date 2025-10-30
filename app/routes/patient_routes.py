from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.utilities.decorators import token_required
import psycopg2.extras

patient_bp = Blueprint("patient_bp", __name__)

#VIEW PROFILE
@patient_bp.route("/profile", methods=["GET"])
@token_required
def view_profile(current_user):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM patients WHERE id = %s", (current_user.id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify({
            "id": patient["id"],
            "full_name": patient["full_name"],
            "email": patient["email"],
            "phone": patient["phone"],
            "date_of_birth": str(patient["date_of_birth"]) if patient["date_of_birth"] else None,
            "first_aid_procedure": patient["first_aid_procedure"],
            "allergies": patient["allergies"],
            "next_of_kin_name": patient["next_of_kin_name"],
            "next_of_kin_phone": patient["next_of_kin_phone"],
            "caregiver_name": patient["caregiver_name"],
            "caregiver_phone": patient["caregiver_phone"]
        }), 200
    finally:
        cursor.close()
        conn.close()

# VIEW MEDICAL RECORDS
@patient_bp.route("/records", methods=["GET"])
@token_required
def view_records(current_user):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM records WHERE patient_id = %s ORDER BY created_at DESC", (current_user.id,))
        records = cursor.fetchall()
        return jsonify([dict(record) for record in records]), 200
    finally:
        cursor.close()
        conn.close()

# ADD MEDICAL RECORD
@patient_bp.route("/records", methods=["POST"])
@token_required
def add_record(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO records (patient_id, diagnosis, prescription, file_url, date_of_visit)
            VALUES (%s, %s, %s, %s, %s)
        """, (current_user.id, data.get("diagnosis"), data.get("prescription"), data.get("file_url"), data.get("date_of_visit")))
        conn.commit()
        return jsonify({"message": "Record added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# VIEW APPOINTMENTS (using reminders table for appointments)
@patient_bp.route("/appointments", methods=["GET"])
@token_required
def view_appointments(current_user):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM reminders WHERE patient_id = %s AND reminder_type = 'appointment' ORDER BY scheduled_time DESC", (current_user.id,))
        appointments = cursor.fetchall()
        return jsonify([dict(appointment) for appointment in appointments]), 200
    finally:
        cursor.close()
        conn.close()

# ADD APPOINTMENT
@patient_bp.route("/appointments", methods=["POST"])
@token_required
def add_appointment(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO reminders (patient_id, caregiver_id, description, reminder_type, scheduled_time, status)
            VALUES (%s, %s, %s, 'appointment', %s, %s)
        """, (current_user.id, data.get("caregiver_id"), data.get("description"), data.get("scheduled_time"), data.get("status", "pending")))
        conn.commit()
        return jsonify({"message": "Appointment added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#  UPDATE PROFILE
@patient_bp.route("/update", methods=["PATCH"])
@token_required
def update_profile(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    protected_fields = ["id", "email", "password"]
    update_data = {k: v for k, v in data.items() if k not in protected_fields}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
        values = list(update_data.values()) + [current_user.id]
        cursor.execute(f"UPDATE patients SET {set_clause} WHERE id = %s", values)
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# VIEW PRESCRIPTIONS
@patient_bp.route("/prescriptions", methods=["GET"])
@token_required
def view_prescriptions(current_user):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("SELECT * FROM prescriptions WHERE patient_id = %s ORDER BY created_at DESC", (current_user.id,))
        prescriptions = cursor.fetchall()
        return jsonify([dict(prescription) for prescription in prescriptions]), 200
    finally:
        cursor.close()
        conn.close()

# ADD PRESCRIPTION
@patient_bp.route("/prescriptions", methods=["POST"])
@token_required
def add_prescription(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO prescriptions (patient_id, medication, dosage, frequency, duration, prescribed_by, date, notes, total_doses)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (current_user.id, data.get("medication"), data.get("dosage"), data.get("frequency"), data.get("duration"), data.get("prescribed_by"), data.get("date"), data.get("notes"), data.get("total_doses", 0)))
        conn.commit()
        return jsonify({"message": "Prescription added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# UPDATE PRESCRIPTION (e.g., mark completed, take dose)
@patient_bp.route("/prescriptions/<int:prescription_id>", methods=["PATCH"])
@token_required
def update_prescription(current_user, prescription_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        update_fields = []
        values = []
        if "completed" in data:
            update_fields.append("completed = %s")
            values.append(data["completed"])
        if "taken_doses" in data:
            update_fields.append("taken_doses = %s")
            values.append(data["taken_doses"])

        if update_fields:
            set_clause = ", ".join(update_fields)
            values.append(prescription_id)
            values.append(current_user.id)
            cursor.execute(f"UPDATE prescriptions SET {set_clause} WHERE id = %s AND patient_id = %s", values)
            conn.commit()
            return jsonify({"message": "Prescription updated successfully"}), 200
        else:
            return jsonify({"error": "No valid fields to update"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# UPDATE EMERGENCY PROFILE
@patient_bp.route("/emergency-profile", methods=["PUT"])
@token_required
def update_emergency_profile(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        update_fields = []
        values = []
        if "blood_type" in data:
            update_fields.append("blood_type = %s")
            values.append(data["blood_type"])
        if "public_visible" in data:
            update_fields.append("public_visible = %s")
            values.append(data["public_visible"])
        if "public_phone_visible" in data:
            update_fields.append("public_phone_visible = %s")
            values.append(data["public_phone_visible"])
        if "visible_fields" in data:
            update_fields.append("visible_fields = %s")
            values.append(data["visible_fields"])

        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            set_clause = ", ".join(update_fields)
            values.append(current_user.id)
            cursor.execute(f"UPDATE emergency_profiles SET {set_clause} WHERE patient_id = %s", values)
            conn.commit()
            return jsonify({"message": "Emergency profile updated successfully"}), 200
        else:
            return jsonify({"error": "No valid fields to update"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
