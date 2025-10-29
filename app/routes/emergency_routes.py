from flask import Blueprint, jsonify
from app.models.emergency_profile import EmergencyProfile

emergency_bp = Blueprint("emergency_bp", __name__)

# PUBLIC EMERGENCY VIEW 
@emergency_bp.route("/emergency/<string:public_id>", methods=["GET"])
def public_emergency_view(public_id):
    profile = EmergencyProfile.query.filter_by(public_id=public_id).first()

    if not profile or not profile.public_visible:
        return jsonify({"error": "Profile not accessible"}), 403

    return jsonify(profile.to_public_dict()), 200