from flask import Blueprint, request, render_template, redirect, url_for, flash
from .. import db
from ..validators import validate_visit, validate_vitals
from ..models import Visit, Vitals, Provider, Patient
from sqlalchemy.exc import IntegrityError
from datetime import datetime

visits_bp = Blueprint("visits", __name__)

@visits_bp.route("/", methods=["GET"])
def get_visits():
    visits=Visit.query.all()
    return render_template("visits/visit_list.html", visits=visits)

@visits_bp.route("/new", methods=["GET"])
def create_visit_form():
    prefill_patient_id = request.args.get("patient_id", "")
    providers=Provider.query.order_by(Provider.last_name, Provider.first_name).all()
    patients=Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    return render_template("visits/visit_update_form.html", visit=None, errors={}, prefill_patient_id=prefill_patient_id, providers=providers, patients=patients)

@visits_bp.route("/create", methods=["POST"])
def create_visit():
    data=request.form.to_dict()
    if data.get("visit_date"):
        data["visit_date"] = datetime.strptime(
            data["visit_date"],
            "%Y-%m-%dT%H:%M"
        )
    errors=validate_visit(data)
    if errors:
        providers=Provider.query.order_by(Provider.last_name, Provider.first_name).all()
        patients=Patient.query.order_by(Patient.last_name, Patient.first_name).all()
        return render_template("visits/visit_update_form.html", visit=None, errors=errors, providers=providers, patients=patients), 422

    visit = Visit(**{k: v for k, v in data.items() if hasattr(Visit, k) and k != "_method"})
    db.session.add(visit)
    db.session.flush()
    visit.visit_num=f"VIS-{visit.visit_id:03d}"
    db.session.commit()
    flash("Created visit record", "success")
    return redirect(url_for("visits.get_visit", visit_id=visit.visit_id))

@visits_bp.route("/<visit_id>", methods=["GET"])
def get_visit(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    vitals=Vitals.query.filter_by(visit_id=visit_id).order_by(Vitals.created_at).all()
    providers=Provider.query.order_by(Provider.last_name, Provider.first_name).all()
    patients=Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    return render_template("visits/visit_detail.html", visit=visit, providers=providers, patients=patients, vitals=vitals)

@visits_bp.route("/<visit_id>/edit", methods=["GET"])
def edit_visit_form(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    providers=Provider.query.order_by(Provider.last_name, Provider.first_name).all()
    patients=Patient.query.order_by(Patient.last_name, Patient.first_name).all()
    return render_template("visits/visit_update_form.html", visit=visit, providers=providers, patients=patients, errors={})

@visits_bp.route("/<visit_id>", methods=["POST"])
def update_visit(visit_id):
    visit=db.get_or_404(Visit, visit_id)
    data=request.form.to_dict()
    if data.get("visit_date"):
        data["visit_date"] = datetime.strptime(
            data["visit_date"],
            "%Y-%m-%dT%H:%M"
        )
    errors=validate_visit(data)
    if errors:
        providers=Provider.query.order_by(Provider.last_name, Provider.first_name).all()
        return render_template("visits/visit_update_form.html", visit=visit, errors=errors, providers=providers), 422

    for key, value in data.items():
        if hasattr(visit, key) and key not in ("visit_id", "_method"):
            setattr(visit, key, value or None)

    db.session.commit()
    flash("Successfully updated visit", "success")
    return redirect(url_for("visits.get_visit", visit_id=visit_id))

@visits_bp.route("/<visit_id>/delete", methods=["POST"])
def delete_visit(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    try:
        db.session.delete(visit)
        db.session.commit()
        flash("Deleted visit", "info")
        return redirect(url_for("visits.get_visits"))
    except IntegrityError:
        db.session.rollback()
        flash("Unable to delete visit. Visit has exisiting vitals", "error")
        return redirect(url_for("visits.get_visit", visit_id=visit_id))

@visits_bp.route("/<visit_id>/vitals/new", methods=["GET"])
def record_vitals_form(visit_id):
    db.get_or_404(Visit, visit_id)
    return render_template("visits/visit_vitals_add_form.html", visit_id=visit_id, errors={})

@visits_bp.route("/<visit_id>/vitals", methods=["POST"])
def record_vitals(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    data = request.form.to_dict()
    data["visit_id"] = visit_id
    errors = validate_vitals(data)
    if errors:
        return render_template("visits/visit_vitals_add_form.html", visit_id=visit_id, errors=errors), 422

    try:
        # Update visit notes to indicate vitals taken
        visit.notes = (visit.notes or "") + f"\n[Vitals recorded by {data.get('recorded_by', 'unknown')}]"

        vitals = Vitals(**{k: v for k, v in data.items() if hasattr(Vitals, k) and k != "_method"})
        db.session.add(vitals)
        db.session.flush()
        vitals.vitals_num=f"VIT-{vitals.vitals_id:03d}"
        db.session.commit()
        flash("Successfully created vitals record.", "success")
        return redirect(url_for("visits.get_visit", visit_id=visit_id))

    except Exception as e:
        db.session.rollback()
        flash(f"Transaction failed, changed not saved: {str(e)}", "error")
        return render_template("visits/visit_vitals_add_form.html", visit_id=visit_id, errors={}), 500


@visits_bp.route("/<visit_id>/vitals/<vitals_id>/delete", methods=["POST"])
def delete_visit_vital(visit_id, vitals_id):
    db.get_or_404(Visit, visit_id)
    vital=Vitals.query.filter_by(vitals_id=vitals_id, visit_id=visit_id).first()
    if not vital:
        flash("Unable to delete visit vital record. No such vital record for this visit")
        return redirect(url_for("visits.get_visit", visit_id=visit_id)), 409
    vital=db.get_or_404(Vitals, vitals_id)
    try:
        db.session.delete(vital)
        db.session.commit()
        flash("Deleted vital record", "info")
        return redirect(url_for("visits.get_visit", visit_id=visit_id))
    except IntegrityError as e:
        db.session.rollback()
        flash(f"Cannot delete visit with existing records: {str(e)}", "error")
        return redirect(url_for("visits.get_visit", visit_id=visit_id))