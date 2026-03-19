from app import db
from datetime import datetime, timezone

class Patient(db.Model):
    __tablename__ = 'PatientData'

    pid = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    city = db.Column(db.String(100), nullable = False)

    @staticmethod
    def generate_patient_id():
        last_patient = Patient.query.order_by(Patient.pid.desc()).first()

        if not last_patient:
            return "PAT001"

        last_number = int(last_patient.patient_id.replace("PAT", ""))
        return f"PAT{last_number + 1:03d}"
    
    
    def __repr__(self):
        return f'Hi {self.name}, Patient Id:{self.patient_id} '
    

class Appointment(db.Model):
    __tablename__ = 'Appointment'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('PatientData.pid'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    doctor = db.Column(db.String(100), nullable = False)
    datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    #adds relationship between two tables(optional)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    department = db.relationship('Department', backref='appointments')

    def __repr__(self):
        return f"Appointment: Doctor={self.doctor} Date={self.datetime}"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
