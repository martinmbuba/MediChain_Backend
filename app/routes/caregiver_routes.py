from flask import Blueprint, request, jsonify
from app.db import get_db_connection, release_db_connection
import psycopg2.extras

caregiver_bp = Blueprint("caregiver_bp", __name__)

@caregiver_bp.route("/register", methods=["POST"])
def register_caregiver():
    data = request.get_json()
    patient_id = data.get("patient_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404

        caregiver_data = (
            data["full_name"],
            data.get("phone"),
            data.get("email"),
            data.get("relation"),
            patient_id
        )
        cursor.execute("""
            INSERT INTO caregivers (full_name, phone, email, relation, patient_id)
            VALUES (%s, %s, %s, %s, %s)
        """, caregiver_data)
        conn.commit()

        return jsonify({"message": "Caregiver registered successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        release_db_connection(conn)

#  VIEW PATIENT RECORDS
@caregiver_bp.route("/<int:patient_id>/records", methods=["GET"])
def caregiver_view_patient_records(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404

        cursor.execute("SELECT * FROM records WHERE patient_id = %s ORDER BY created_at DESC", (patient_id,))
        records = cursor.fetchall()
        return jsonify([dict(record) for record in records]), 200
    finally:
        cursor.close()
        release_db_connection(conn)

# VIEW PATIENT APPOINTMENTS
@caregiver_bp.route("/<int:patient_id>/appointments", methods=["GET"])
def caregiver_view_patient_appointments(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404

        cursor.execute("SELECT * FROM reminders WHERE patient_id = %s AND reminder_type = 'appointment' ORDER BY scheduled_time DESC", (patient_id,))
        appointments = cursor.fetchall()
        return jsonify([dict(appointment) for appointment in appointments]), 200
    finally:
        cursor.close()
        release_db_connection(conn)

# ADD APPOINTMENT FOR PATIENT
@caregiver_bp.route("/<int:patient_id>/appointments", methods=["POST"])
def caregiver_add_appointment(patient_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404

        cursor.execute("""
            INSERT INTO reminders (patient_id, caregiver_id, description, reminder_type, scheduled_time, status)
            VALUES (%s, %s, %s, 'appointment', %s, %s)
        """, (patient_id, data.get("caregiver_id"), data.get("description"), data.get("scheduled_time"), data.get("status", "pending")))
        conn.commit()
        return jsonify({"message": "Appointment added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        release_db_connection(conn)
