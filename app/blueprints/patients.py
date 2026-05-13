from flask import Blueprint, request, render_template, flash, redirect, url_for
from .. import db
from ..validators import validate_patient, validate_diagnosis
from ..models import Patient, Diagnosis, Visit
from sqlalchemy.exc import IntegrityError

patients_bp=Blueprint("patients", __name__, url_prefix="/patients")

@patients_bp.route("/create", methods=["POST"])
def create_patient():
    data=request.form.to_dict()
    errors=validate_patient(data)
    if errors:
        return render_template("patients/patient_edit_form.html", patient=None, errors=errors), 422

    patient = Patient(**{k: v for k, v in data.items() if hasattr (Patient, k)})
    db.session.add(patient)
    db.session.commit()
    flash("Successfully created patient", "success")
    return redirect(url_for("patients.get_patient", patient_id=patient.patient_id))

@patients_bp.route("/new", methods=["GET"])
def create_patient_form():
    return render_template("patients/patient_edit_form.html", patient=None, errors={})

@patients_bp.route("/all", methods=["GET"])
def get_patients():
    patients=Patient.query.all()
    return render_template("patients/patients_list.html", patients=patients)

@patients_bp.route("/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    diagnoses=Diagnosis.query.filter_by(patient_id=patient_id).all()
    visits=Visit.query.filter_by(patient_id=patient_id).order_by(Visit.visit_date.desc()).all()
    return render_template("patients/patient_detail.html", patient=patient, diagnoses=diagnoses, visits=visits)

@patients_bp.route("/<patient_id>/update", methods=["GET"])
def edit_patient_form(patient_id):
    patient = db.get_or_404(Patient, patient_id)
    return render_template("patients/patient_edit_form.html", patient=patient, errors={})

@patients_bp.route("/<patient_id>", methods=["POST"])
def update_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    data=request.form.to_dict()
    errors=validate_patient({**data, "patient_id": patient_id})
    if errors:
        return render_template("patients/patient_edit_form.html", patient=patient, errors=errors), 422

    for key, value in data.items():
        if hasattr(patient, key) and key not in ("patient_id", "_method"):
            setattr(patient, key, value or None)

    db.session.commit()
    flash("Successfully updated patient", "success")
    return redirect(url_for("patients.get_patient", patient_id=patient_id))

@patients_bp.route("/<patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        flash("Deleted patient", "info")
        return redirect(url_for("patients.get_patients"))
    except IntegrityError:
        db.session.rollback()
        flash("Unable to delete patient. Patient has existing visits or diagnoses", "error")
        return redirect(url_for("patients.get_patient", patient_id=patient_id))


@patients_bp.route("/<patient_id>/diagnoses/new", methods=["GET"])
def create_patient_diagnosis_form(patient_id):
    db.get_or_404(Patient, patient_id)
    return render_template("patients/patient_add_diagnosis_form.html", patient_id=patient_id, errors={})

@patients_bp.route("/<patient_id>/diagnoses", methods=["POST"])
def create_patient_diagnoses(patient_id):
    db.get_or_404(Patient, patient_id)
    data=request.form.to_dict()
    data["patient_id"]=patient_id
    errors=validate_diagnosis(data)
    if errors:
        return render_template("patients/patient_add_diagnosis_form.html", patient_id=patient_id, errors=errors), 422

    diagnosis = Diagnosis(**{k: v for k,v in data.items() if hasattr (Diagnosis, k)})
    db.session.add(diagnosis)
    db.session.commit()
    flash("Successfully added diagnosis", "success")
    return redirect(url_for("patients.get_patient", patient_id=patient_id))

@patients_bp.route("/<patient_id>/diagnosis", methods=["POST"])
def delete_patient_diagnosis(patient_id, diagnosis_id):
    patient=db.get_or_404(Patient, patient_id)
    if diagnosis_id not in patient["diagnosis"]:
        flash("Unable to delete patient diagnosis. No such diagnosis for this patient", "error")
        return redirect(url_for("patients.get_patient", patient_id=patient_id))
    diagnosis=db.get_or_404(Diagnosis, diagnosis_id)
    try:
        db.session.delete(diagnosis)
        db.session.commit()
        flash("Deleted patient diagnosis.", "info")
        return redirect(url_for("patients.get_patients", patient_id=patient_id))
    except IntegrityError as e:
        db.session.rollback()
        flash("Unable to delete diagnosis", "error")
        return redirect(url_for("patients.get_patient", patient_id=patient_id))