from flask import render_template, session, request, redirect, url_for, flash
from sqlalchemy import func
from models import Patient, Appointment, Doctor, Department
from datetime import date

def register_routes(app,db):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            form_type = request.form.get('form_type')

            # ------------------ PATIENT LOGIN ------------------
            if form_type == 'patient':
                patient_id = request.form.get('patient_id')
                name = request.form.get('name')

                patient = Patient.query.filter(
                    Patient.patient_id == patient_id,
                    func.lower(Patient.name) == name.lower()
                ).first()

                if patient:
                    session['patient_pid'] = patient.pid
                    return redirect(url_for('patient_details'))
                else:
                    flash("Invalid Patient ID or Name", "danger")

            # ------------------ DOCTOR LOGIN ------------------
            elif form_type == 'doctor':
                email = request.form.get('doc_email')
                name = request.form.get('doc_name')

                doctor = Doctor.query.filter(
                    Doctor.email == email,
                    func.lower(Doctor.name) == name.lower()
                ).first()

                if doctor:
                    session['doctor_id'] = doctor.id
                    return redirect(url_for('doctor_details'))
                else:
                    flash("Invalid Doctor Credentials", "danger")

        return render_template('index.html')

    #patient detail route
    @app.route('/patient_details')
    def patient_details():
        if 'patient_pid' not in session:
            return redirect(url_for('index'))

        client = Patient.query.get(session['patient_pid'])

        if not client:
            return redirect(url_for('index'))

        # Query all appointments for this patient
        appointments = Appointment.query.filter_by(patient_id=client.pid).all()

        return render_template('patient.html', client=client, appointments=appointments)

    #register patient
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            new_patient_id = Patient.generate_patient_id()
            name = request.form['name']
            age = request.form ['age']
            city = request.form['city']

            patient = Patient (patient_id = new_patient_id, name = name, age=age, city=city)

            db.session.add(patient)
            db.session.commit()

            flash(f"Patient <strong> {name} </strong> registered successfully with ID <strong>{new_patient_id}</strong>! Kindly <strong>save your Patient Id</strong> as it will not regenerate", "success")
            return redirect(url_for('index'))  # Redirect to avoid form resubmission

        

        return render_template('register.html')
    
    

    #make appointment
    @app.route('/appointment', methods=['GET', 'POST'])
    def appointment():
        if 'patient_pid' not in session:
            return redirect(url_for('index'))

        patient = Patient.query.get(session['patient_pid'])
        doctors = Doctor.query.all()  # get all doctors
        departments = Department.query.all()  # Fetch all departments

        if request.method == 'POST':
            dept_id = request.form['dept_id']
            doctor_id = request.form['doctor_id']

            appointment = Appointment(
                patient_id=patient.pid,
                dept_id=dept_id,
                doctor_id=doctor_id
            )

            db.session.add(appointment)
            db.session.commit()

            flash("Appointment booked successfully!", "success")
            return redirect(url_for('patient_details'))

        return render_template('appointment.html', patient=patient, doctors=doctors, departments=departments)


    #doctor_details
    @app.route('/doctor_details')
    def doctor_details():
        if 'doctor_id' not in session:
            return redirect(url_for('index'))

        doctor = Doctor.query.get(session['doctor_id'])
        if not doctor:
            return redirect(url_for('index'))

        today = date.today()

        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            db.func.date(Appointment.datetime) == today
        ).all()


        return render_template('doctor.html',doctor=doctor,appointments=appointments)



    #logout session
    @app.route('/logout')
    def logout():
        session.clear()   # clears all session data
        return redirect(url_for('index'))
