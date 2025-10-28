from .auth_routes import auth_bp
from .patient_routes import patient_bp
from .caregiver_routes import caregiver_bp
from .emergency_routes import emergency_bp


def register_routes(app):
    """Register all API blueprints to the Flask app."""
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(caregiver_bp, url_prefix="/api/caregiver")
    app.register_blueprint(emergency_bp, url_prefix="/api/emergency")
