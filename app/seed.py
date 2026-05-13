from datetime import date, datetime
import click
from . import db
from .models import *

def register_seed_command(app):
    @app.cli.command("seed")
    @click.option("--reset", is_flag=True, help="Drop and recreate all tables before seeding")
    def seed(reset):
        if reset:
            click.echo("Dropping all tables")
            db.drop_all()
            db.create_all()
            click.echo("Tables recreated")

        _seed_all()
        click.echo("Successfully entered seed data")


def _seed_all():
    _seed_icd()
    _seed_patients()
    _seed_providers()
    _seed_provider_specialties()
    _seed_provider_state_licenses()
    _seed_visits()
    _seed_vitals()
    _seed_diagnoses()

def _seed_icd():
    records=[
        ICD(icd_code="Z00.00", description="Encounter for general adult medical examination"),
        ICD(icd_code="R07.9",  description="Chest pain, unspecified"),
        ICD(icd_code="J06.9",  description="Acute upper respiratory infection, unspecified"),
        ICD(icd_code="R00.2",  description="Palpitations"),
        ICD(icd_code="E11.9",  description="Type 2 diabetes mellitus without complications"),
        ICD(icd_code="M79.36", description="Pain in left lower leg"),
        ICD(icd_code="I10",    description="Essential (primary) hypertension"),
    ]
    _bulk_insert(records, "ICD codes")

def _seed_patients():
    records=[
        Patient(
            patient_id="PAT-001",
            first_name="Bob",
            last_name="Smith",
            date_of_birth=date(1968, 4, 12),
            email="bob.smith@email.com",
            phone_number="555-201-1001",
        ),
        Patient(
            patient_id="PAT-002",
            first_name="Alice",
            last_name="Jones",
            date_of_birth=date(1982, 9, 30),
            email="alice.jones@email.com",
            phone_number="555-201-1002",
        ),
        Patient(
            patient_id="PAT-003",
            first_name="Charlie",
            last_name="Owens",
            date_of_birth=date(1995, 11, 7),
            email="charlie.owens@email.com",
            phone_number="555-201-1003",
        ),
        Patient(
            patient_id="PAT-004",
            first_name="Dave",
            last_name="Jabots",
            date_of_birth=date(1955, 3, 22),
            email="dave.jabots@email.com",
            phone_number="555-201-1004",
        ),
        Patient(
            patient_id="PAT-005",
            first_name="Ellen",
            last_name="Hunt",
            date_of_birth=date(2001, 6, 15),
            email="ellen.hunt@email.com",
            phone_number="555-201-1005",
        ),
    ]
    _bulk_insert(records, "Patients")

def _seed_providers():
    records=[
        Provider(national_provider_identifier="1234567890", first_name="Frank",    last_name="Daniels",  phone_number="555-300-2001"),
        Provider(national_provider_identifier="1234567891", first_name="Grace",    last_name="Williams", phone_number="555-300-2002"),
        Provider(national_provider_identifier="1234567892", first_name="Isabella", last_name="Potter",   phone_number="555-300-2003"),
        Provider(national_provider_identifier="1234567893", first_name="Henry",    last_name="White",    phone_number="555-300-2004"),
        Provider(national_provider_identifier="1234567894", first_name="Jane",     last_name="Doe",      phone_number="555-300-2005"),
    ]
    _bulk_insert(records, "Providers")

def _seed_provider_specialties():
    records=[
        ProviderSpecialty(national_provider_identifier="1234567890", healthcare_provider_taxonomy_code="207Q00000X"),
        ProviderSpecialty(national_provider_identifier="1234567891", healthcare_provider_taxonomy_code="207R00000X"),
        ProviderSpecialty(national_provider_identifier="1234567892", healthcare_provider_taxonomy_code="207N00000X"),
        ProviderSpecialty(national_provider_identifier="1234567893", healthcare_provider_taxonomy_code="207X00000X"),
        ProviderSpecialty(national_provider_identifier="1234567894", healthcare_provider_taxonomy_code="207RE0101X"),
    ]
    _bulk_insert(records, "Provider Specialties")

def _seed_provider_state_licenses():
    records=[
        ProviderStateLicense(issue_state="Maryland", national_provider_identifier="1234567890", state_license="MD-100421"),
        ProviderStateLicense(issue_state="Maryland", national_provider_identifier="1234567891", state_license="MD-100422"),
        ProviderStateLicense(issue_state="Maryland", national_provider_identifier="1234567892", state_license="MD-100423"),
        ProviderStateLicense(issue_state="Maryland", national_provider_identifier="1234567893", state_license="MD-100424"),
        ProviderStateLicense(issue_state="Maryland", national_provider_identifier="1234567894", state_license="MD-100425"),
    ]
    _bulk_insert(records, "Provider State Licenses")

_PRV_TO_NPI={
    "PRV-001": "1234567890",
    "PRV-002": "1234567891",
    "PRV-003": "1234567892",
    "PRV-004": "1234567893",
    "PRV-005": "1234567894",
}

def _seed_visits():
    records=[
        Visit(visit_id="VST-001", patient_id="PAT-001", national_provider_identifier=_PRV_TO_NPI["PRV-001"], visit_date=datetime(2024, 1, 15, 9,  0),  visit_reason="Annual physical"),
        Visit(visit_id="VST-002", patient_id="PAT-002", national_provider_identifier=_PRV_TO_NPI["PRV-002"], visit_date=datetime(2024, 2, 10, 10, 30), visit_reason="Chest tightness"),
        Visit(visit_id="VST-003", patient_id="PAT-003", national_provider_identifier=_PRV_TO_NPI["PRV-001"], visit_date=datetime(2024, 3,  5,  8, 45), visit_reason="Persistent cough"),
        Visit(visit_id="VST-004", patient_id="PAT-004", national_provider_identifier=_PRV_TO_NPI["PRV-003"], visit_date=datetime(2024, 3, 20, 14,  0), visit_reason="Palpitations"),
        Visit(visit_id="VST-005", patient_id="PAT-005", national_provider_identifier=_PRV_TO_NPI["PRV-005"], visit_date=datetime(2024, 4,  8, 11, 15), visit_reason="High blood sugar symptoms"),
        Visit(visit_id="VST-006", patient_id="PAT-001", national_provider_identifier=_PRV_TO_NPI["PRV-004"], visit_date=datetime(2024, 5, 14, 13,  0), visit_reason="Knee pain after running"),
        Visit(visit_id="VST-007", patient_id="PAT-002", national_provider_identifier=_PRV_TO_NPI["PRV-002"], visit_date=datetime(2024, 6,  1,  9, 30), visit_reason="Blood pressure check"),
    ]
    _bulk_insert(records, "Visits")

def _seed_vitals():
    records=[
        Vitals(vitals_id="VTL-001", visit_id="VST-001", height=65, weight=158.0, systolic=118, diastolic=76, temperature=98.4, heart_rate=68, pain_level=2, recorded_by="Frank Daniels"),
        Vitals(vitals_id="VTL-002", visit_id="VST-002", height=71, weight=195.0, systolic=142, diastolic=90, temperature=98.6, heart_rate=92, pain_level=6, recorded_by="Grace Williams"),
        Vitals(vitals_id="VTL-003", visit_id="VST-003", height=62, weight=121.0, systolic=110, diastolic=70, temperature=99.1, heart_rate=74, pain_level=3, recorded_by="Frank Daniels"),
        Vitals(vitals_id="VTL-004", visit_id="VST-004", height=68, weight=176.0, systolic=130, diastolic=84, temperature=98.2, heart_rate=88, pain_level=4, recorded_by="Isabella Potter"),
        Vitals(vitals_id="VTL-005", visit_id="VST-005", height=63, weight=209.0, systolic=138, diastolic=88, temperature=98.8, heart_rate=80, pain_level=5, recorded_by="Jane Doe"),
        Vitals(vitals_id="VTL-006", visit_id="VST-006", height=72, weight=200.0, systolic=122, diastolic=78, temperature=97.9, heart_rate=72, pain_level=7, recorded_by="Henry White"),
        Vitals(vitals_id="VTL-007", visit_id="VST-007", height=65, weight=163.0, systolic=148, diastolic=94, temperature=98.5, heart_rate=70, pain_level=3, recorded_by="Grace Williams"),
    ]
    _bulk_insert(records, "Vitals")

_VISIT_TO_PATIENT={
    "VST-001": "PAT-001",
    "VST-002": "PAT-002",
    "VST-003": "PAT-003",
    "VST-004": "PAT-004",
    "VST-005": "PAT-005",
    "VST-006": "PAT-001",
    "VST-007": "PAT-002",
}

def _seed_diagnoses():
    rows=[
        ("DGN-001", "VST-001", "Z00.00", "resolved"),
        ("DGN-002", "VST-002", "R07.9",  "active"),
        ("DGN-003", "VST-003", "J06.9",  "resolved"),
        ("DGN-004", "VST-004", "R00.2",  "active"),
        ("DGN-005", "VST-005", "E11.9",  "chronic"),
        ("DGN-006", "VST-006", "M79.36", "active"),
        ("DGN-007", "VST-007", "I10",    "active"),
    ]
    records=[
        Diagnosis(
            diagnosis_id=diagnosis_id,
            patient_id=_VISIT_TO_PATIENT[visit_id],
            icd_code=icd_code,
            status=status,
        )
        for diagnosis_id, visit_id, icd_code, status in rows
    ]
    _bulk_insert(records, "Diagnoses")

def _bulk_insert(records: list, label: str):
    inserted=0
    skipped=0
    for record in records:
        if db.session.get(type(record), _primary_key(record)):
            skipped+=1
        else:
            db.session.add(record)
            inserted+=1
    db.session.commit()
    click.echo(f"  {label}: {inserted} inserted, {skipped} skipped.")

def _primary_key(record):
    mapper=record.__class__.__mapper__
    pk_cols=mapper.primary_key
    values=tuple(getattr(record, col.key) for col in pk_cols)
    return values[0] if len(values) == 1 else values