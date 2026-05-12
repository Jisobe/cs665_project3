from flask import Blueprint, request, jsonify
from .. import db
from ..validators import validate_visit, validate_vitals
from ..models import Visit, Vitals
from sqlalchemy.exc import IntegrityError

visits_bp = Blueprint("visits", __name__, url_prefix="/visits")

@visits_bp.route("/create", methods=["POST"])
def create_visit():
    data=request.get_json()
    errors=validate_visit(data)
    if errors:
        return jsonify({"errors": errors}), 422

    visit = Visit(**{k: data[k] for k in data if hasattr (Visit, k)})
    db.session.add(visit)
    db.session.commit()
    return jsonify({"visit_id": visit.visit_id}), 201

@visits_bp.route("/<visit_id>", methods=["GET"])
def get_visit(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    return jsonify({
        "visit_id": visit.visit_id,
        "visit_id": visit.visit_id,
        "national_provider_identifier": visit.national_provider_identifier,
        "visit_date": visit.visit_date.isoformat() if visit.visit_date else None,
        "visit_reason": visit.visit_reason,
        "notes": visit.notes,
        "vitals": [
            {
                "vitals_id": vital.vitals_id,
                "height": vital.height,
                "weight": vital.weight,
                "systolic": vital.systolic,
                "diastolic": vital.diastolic,
                "temperature": vital.temperature,
                "heart_rate": vital.heart_rate,
                "pain_level": vital.pain_level,
                "recorded_by": vital.recorded_by,
                "created_at": vital.created_at.isoformat(),
            }
            for vital in visit.vitals
        ],
    })

@visits_bp.route("/<visit_id>", methods=["PATCH"])
def update_visit(visit_id):
    visit=db.get_or_404(Visit, visit_id)
    data=request.get_json()
    errors=validate_visit(data)
    if errors:
        return jsonify({"errors": errors}), 422

    for key, value in data.items():
        if hasattr(visit, key) and key != "visit_id":
            setattr(visit, key, value)

    db.session.commit()
    return jsonify({"Message: visit updated"})

@visits_bp.route("/<visit_id>", methods=["DELETE"])
def delete_visit(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    try:
        db.session.delete(visit)
        db.session.commit()
        return "", 204
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Unable to delete visit. Visit has exisiting vitals"}), 409

@visits_bp.route("/<visit_id>/vitals", methods=["POST"])
def record_vitals(visit_id):
    visit = db.get_or_404(Visit, visit_id)
    data = request.get_json()
    data["visit_id"] = visit_id
    errors = validate_vitals(data)
    if errors:
        return jsonify({"errors": errors}), 422

    try:
        # Update visit notes to indicate vitals taken
        visit.notes = (visit.notes or "") + f"\n[Vitals recorded by {data.get('recorded_by', 'unknown')}]"

        vitals = Vitals(**{k: data[k] for k in data if hasattr(Vitals, k)})
        db.session.add(vitals)

        db.session.commit()
        return jsonify({"vitals_id": vitals.vitals_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Transaction failed, changes not saved.", "detail": str(e)}), 500


@visits_bp.route("/<visit_id>/vitals", methods=["DELETE"])
def delete_visit_vital(visit_id, vital_id):
    visit = db.get_or_404(Visit, visit_id)
    if vital_id not in visit["vitals"]:
        return jsonify({"error": "Unable to delete visit vital record. No such vital record for this visit"}), 409
    vital=db.get_or_404(Vitals, vital_id)
    try:
        db.session.delete(vital)
        db.session.commit()
        return "", 204
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Unable to delete visit vital record", "detail": str(e)}), 409