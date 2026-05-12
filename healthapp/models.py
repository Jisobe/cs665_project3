from . import db
from datetime import datetime, timezone

def dt_now():
    return datetime.now(timezone.utc)

class Patient(db.Model):
    __tablename__="patient"
    patient_id=db.Column(db.String(20), primary_key=True)
    date_of_birth=db.Column(db.Date)
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    email=db.Column(db.String(100))
    phone_number=db.Column(db.String(20))
    created_at=db.Column(db.DateTime, nullable=False, default=dt_now)
    updated_at=db.Column(db.DateTime, nullable=False, default=dt_now, onupdate=dt_now)
    visits=db.relationship("Visit", back_populates="patient", passive_deletes=True)
    diagnosis=db.relationship("Diagnosis", back_populates="patient", passive_deletes=True)

class Provider(db.Model):
    __tablename__="provider"
    national_provider_identifier=db.Column(db.String(10), primary_key=True)
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    phone_number=db.Column(db.String(20))
    created_at=db.Column(db.DateTime, nullable=False, default=dt_now)
    updated_at=db.Column(db.DateTime, nullable=False, default=dt_now, onupdate=dt_now)
    specialties=db.relationship("ProviderSpecialty", back_populates="provider", cascade="all, delete-orphan")
    state_licenses=db.relationship("ProviderStateLicense", back_populates="provider", cascade="all, delete-orphan")
    visits=db.relationship("Visit", back_populates="provider", passive_deletes=True)

class ProviderSpecialty(db.Model):
    __tablename__="provider_specialty"
    national_provider_identifier=db.Column(db.String(10), db.ForeignKey("provider.national_provider_identifier"),primary_key=True)
    healthcare_provider_taxonomy_code=db.Column(db.String(10), primary_key=True)
    provider=db.relationship("Provider", back_populates="specialties")

class ProviderStateLicense(db.Model):
    __tablename__="provider_state_license"
    issue_state=db.Column(db.String(25), primary_key=True)
    national_provider_identifier=db.Column(db.String(10), db.ForeignKey("provider.national_provider_identifier"),primary_key=True)
    state_license=db.Column(db.String(20), nullable=False)
    provider=db.relationship("Provider", back_populates="state_license")

class Visit(db.Model):
    __tablename__="visit"
    visit_id=db.Column(db.String(20), primary_key=True)
    patient_id=db.Column(db.String(20), db.ForeignKey("patient.patient_id", ondelete="RESTRICT"), nullable=False)
    national_provider_identifier=db.Column(db.String(10), db.ForeignKey("provider.national_provider_identifier", ondelete="RESTRICT"),nullable=False)
    visit_date=db.Column(db.DateTime)
    visit_reason=db.Column(db.Text)
    created_at=db.Column(db.DateTime, nullable=False, default=dt_now)
    updated_at=db.Column(db.DateTime, nullable=False, default=dt_now, onupdate=dt_now)
    patient=db.relationship("Patient", back_populates="visits")
    provider=db.relationship("Provider", back_populates="visits")
    vitals=db.relationship("Vitals", back_populates="visits")

class Vitals(db.Model):
    __tablename__="vitals"
    vitals_id=db.Column(db.String(20), primary_key=True)
    visit_id=db.Column(db.String(20), db.ForeignKey("visit.visit_id"), nullable=False)
    height=db.Column(db.Integer)
    weight=db.Column(db.Float)
    systolic=db.Column(db.Integer)
    diastolic=db.Column(db.Integer)
    temperature=db.Column(db.Float)
    heart_rate=db.Column(db.Integer)
    pain_level=db.Column(db.Integer, db.CheckConstraint("pain_level BETWEEN 0 AND 10"))
    recorded_by=db.Column(db.String(100))
    created_at=db.Column(db.DateTime, nullable=False, default=dt_now)
    visit=db.relationship("Visit", back_populates="vitals")

class ICD(db.Model):
    __tablename__="icd"
    icd_code=db.Column(db.String(20), primary_key=True)
    description=db.Column(db.Text)
    diagnosis=db.relationship("Diagnosis", back_populates="icd")

class Diagnosis(db.Model):
    __tablename__="diagnosis"
    diagnosis_id=db.Column(db.String(20), primary_key=True)
    patient_id=db.Column(db.String(20), db.ForeignKey("patient.patient_id", ondelete="RESTRICT"), nullable=False)
    icd_code=db.Column(db.String(20), db.ForeignKey("icd.icd_code"), nullable=False)
    status=db.Column(db.String(20))
    created_at=db.Column(db.DateTime, nullable=False, default=dt_now)
    updated_at=db.Column(db.DateTime, nullable=False, default=dt_now, onupdate=dt_now)
    patient=db.relationship("Patient", back_populates="diagnosis")
    icd=db.relationship("ICD", back_populates="diagnosis")
