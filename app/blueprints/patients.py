from flask import Blueprint, request, jsonify
from .. import db
from ..validators import validate_patient, validate_diagnosis
from ..models import Patient, Diagnosis
from sqlalchemy.exc import IntegrityError

patients_bp=Blueprint("patients", __name__)

@patients_bp.route("/", methods=["POST"])
def create_patient():
    data=request.get_json()
    errors=validate_patient(data)
    if errors:
        return jsonify({"errors": errors}), 422

    patient = Patient(**{k: data[k] for k in data if hasattr (Patient, k)})
    db.session.add(patient)
    db.session.commit()
    return jsonify({"patient_id": patient.patient_id}), 201

@patients_bp.route("/", methods=["GET"])
def get_patients():
    patients=Patient.query.all()
    return jsonify([
        {
            "patient_id": patient.patient_id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email if patient.email else None,
            "phone_number": patient.phone_number if patient.phone_number else None,
            "date_of_birth": patient.date_of_birth

        }
        for patient in patients
    ])

@patients_bp.route("/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    return jsonify([
        {
            "patient_id": patient.patient_id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email if patient.email else None,
            "phone_number": patient.phone_number if patient.phone_number else None,
            "date_of_birth": patient.date_of_birth

        }
    ])

@patients_bp.route("/<patient_id>", methods=["PATCH"])
def update_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    data=request.get_json()
    errors=validate_patient(data)
    if errors:
        return jsonify({"errors": errors}), 422

    for key, value in data.items():
        if hasattr(patient, key) and key != "patient_id":
            setattr(patient, key, value)

    db.session.commit()
    return jsonify({"Message: Patient updated"})

@patients_bp.route("/<patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patient=db.get_or_404(Patient, patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        return "", 204
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Unable to delete patient. Patient has existing visits or diagnoses"}), 409

@patients_bp.route("/<patient_id>/diagnoses", methods=["GET"])
def get_patient_diagnoses(patient_id):
    db.get_or_404(Patient, patient_id)
    diagnoses = Diagnosis.query.filter_by(patient_id=patient_id).all()
    return jsonify([
        {
            "diagnosis_id": diagnosis.diagnosis_id,
            "icd_code": diagnosis.icd_code,
            "status": diagnosis.status,
            "created_at": diagnosis.created_at.isoformat()
        }
        for diagnosis in diagnoses
    ])

@patients_bp.route("/<patient_id>/diagnoses", methods=["POST"])
def create_patient_diagnoses(patient_id):
    db.get_or_404(Patient, patient_id)
    data=request.get_json()
    data["patient_id"]=patient_id
    errors=validate_diagnosis(data)
    if errors:
        return jsonify({"errors": errors}), 422

    diagnosis = Diagnosis(**{k: data[k] for k in data if hasattr (Diagnosis, k)})
    db.session.add(diagnosis)
    db.session.commit()
    return jsonify({"diagnosis_id": diagnosis.diagnosis_id}), 201