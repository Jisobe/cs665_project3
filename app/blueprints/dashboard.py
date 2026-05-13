from flask import Blueprint, render_template
from .. import db
from ..models import Patient, Provider, Visit, Vitals, Diagnosis
from sqlalchemy import func

dashboard_bp=Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
def dashboard_summary():
    totals={
        "total_patients": db.session.execute(func.count(Patient.patient_id)).scalar(),
        "total_providers": db.session.execute(func.count(Provider.national_provider_identifier)).scalar(),
        "total_visits": db.session.execute(func.count(Visit.visit_id)).scalar(),
        "total_diagnoses": db.session.execute(func.count(Diagnosis.diagnosis_id_id)).scalar()
    }

    vitals_avg=db.session.query(
        func.round(func.avg(Vitals.height), 2).label("avg_height"),
        func.round(func.avg(Vitals.weight), 2).label("avg_weight"),
        func.round(func.avg(Vitals.systolic), 0).label("avg_sys"),
        func.round(func.avg(Vitals.diastolic), 0).label("avg_dia"),
        func.round(func.avg(Vitals.heart_rate), 0).label("avg_bpm"),
        func.round(func.avg(Vitals.temperature), 2).label("avg_temp"),
        func.round(func.avg(Vitals.pain_level), 2).label("avg_pain"),
    ).one()

    vitals_averages={
        "avg_height": vitals_avg.avg_height,
        "avg_weight": vitals_avg.avg_weight,
        "avg_sys": vitals_avg.avg_sys,
        "avg_dia": vitals_avg.avg_dia,
        "avg_temp": vitals_avg.avg_temp,
        "avg_bpm": vitals_avg.avg_bpm,
        "avg_pain": vitals_avg.avg_pain,
    }

    num_visits_per_provider=db.session.query(
        Provider.national_provider_identifier,
        Provider.first_name,
        Provider.last_name,
        func.count(Visit.visit_id).label("provider_vistit_count")
    ).join(Visit, isouter=True).group_by(Provider.national_provider_identifier).all()

    visits_per_provider=[
            {
                "npi": row.national_provider_identifier,
                "name": f"{row.first_name} {row.last_name}",
                "visit_count": row.provider_vistit_count
            } for row in num_visits_per_provider
        ]

    diagnosis_count_by_status=db.session.query(
        Diagnosis.status,
        func.count(Diagnosis.diagnosis_id).label("diagnosis_status_count")
    ).group_by(Diagnosis.status).all()

    diagnosis_by_status=[
            {"status": row.status,
             "count": row.count
            } for row in diagnosis_count_by_status
        ]

    return render_template(
        "dashboard/index.html",
        totals=totals,
        vitals_averages=vitals_averages,
        visits_per_provider=visits_per_provider,
        diagnosis_by_status=diagnosis_by_status
    )