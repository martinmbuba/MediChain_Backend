from .auth_routes import auth_bp
from .patient_routes import patient_bp
from .doctor_routes import doctor_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctor")
