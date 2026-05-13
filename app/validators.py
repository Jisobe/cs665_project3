import re
from datetime import date
from .models import Patient
from datetime import datetime

STATES=[
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"]

STATUS=["active", "resolved", "chronic", "remission", "acute", "suspended"]

def validate_patient(data):
    errors={}
    dob=data.get("date_of_birth")
    first_name=(data.get("first_name") or "").strip()
    last_name=(data.get("last_name") or "").strip()
    email=(data.get("email") or "").strip()
    phone_number=(data.get("phone_number") or "").strip()

    if not first_name:
        errors["first_name"]="Missing Required Field: First name"
    elif len(first_name)>50:
        errors["first_name"]=("Invalid Length: First name cannot have more that 50 characters")

    if not last_name:
        errors["last_name"]=("Missing Required Field: Last name")
    elif len(last_name)>50:
        errors["last_name"]=("Invalid Length: Last name cannot have more that 50 characters")

    if not email and not phone_number:
        errors["email_and_phone"]=("Missing Contact Information: Patient requires at least one contact method")

    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors["email"]=("Invalid Entry: Email address is not valid")

    if phone_number and not re.match(r"^[\d\s\-\(\)\+\.]{7,20}$", phone_number):
        errors["phone_number"]=("Invalid Entry: Phone number is not valid")

    if dob:
        try:
            # parsed=date.fromisoformat(dob)
            if dob > date.today():
                errors["date_of_birth"]=("Invalid Entry: Date of birth cannot be in future")
        except ValueError:
            errors["date_of_birth"]=("Invalid Entry: Date of birth is not valid")
    else:
        errors["date_of_birth"]=("Missing Required Field: Date of Birth")

    return errors

def validate_provider(data):
    errors={}
    npi=(data.get("national_provider_identifier") or "").strip()
    first_name=(data.get("first_name") or "").strip()
    last_name=(data.get("last_name") or "").strip()
    phone_number=(data.get("phone_number") or "").strip()

    if not npi:
        errors["npi"]="Missing Required Field: National Provider Identifier"
    elif not re.match(r"^\d{10}$", npi):
        errors["npi"]=("Invalid Length: National Provider Identifier must be 10 digits")

    if not first_name:
        errors["first_name"]=("Missing Required Field: First name")
    elif len(first_name)>50:
        errors["first_name"]=("Invalid Length: First name cannot have more that 50 characters")

    if not last_name:
        errors["last_name"]=("Missing Required Field: Last name")
    elif len(last_name)>50:
        errors["last_name"]=("Invalid Length: Last name cannot have more that 50 characters")

    if phone_number and not re.match(r"^[\d\s\-\(\)\+\.]{7,20}$", phone_number):
        errors["phone_number"]=("Invalid Entry: Phone number is not valid")

    return errors

def validate_provider_specialty(data):
    errors={}
    htc=(data.get("healthcare_provider_taxonomy_code") or "").strip()

    if not htc:
        errors["htc"]="Missing Required Field: Healthcare Provider Taxonomy Code"
    elif not re.match(r"^[a-zA-Z\d]{10}$", htc):
        errors["htc"]=("Invalid Length: Healthcare Provider Taxonomy Code must be 10 alphanumeric characters")

    return errors

def validate_state_license(data):
    errors={}
    state=(data.get("issue_state") or "").strip()
    license=(data.get("state_license") or "").strip()

    if not state:
        errors["state"]=("Missing Required Field: Issue State")
    elif state not in STATES:
        errors["state"]=("Invalid Entry: Issue state is not valid")

    if not license:
        errors["license"]=("Missing Required Field: State License")

    return errors

def validate_visit(data):
    errors={}
    patient_id=(data.get("patient_id") or "").strip()
    npi=(data.get("national_provider_identifier") or "").strip()
    visit_date=(data.get("visit_date") or "")
    reason=(data.get("visit_reason") or "").strip()

    if not patient_id:
        errors["patient_id"]=("Missing Required Field: Patient ID")

    if not npi:
        errors["national_provider_identifier"]=("Missing Required Field: National Provider Identifier")

    if visit_date:
        try:
            # parsed=date.fromisoformat(visit_date)
            if visit_date > datetime.now():
                errors["visit_date"]=("Invalid Entry: Visit date cannot be in future")
        except ValueError:
            errors["visit_date"]=("Invalid Entry: Visit date is not valid")
    else:
        errors["visit_date"]=("Missing Required Field: Date of Birth")

    if not reason:
        errors["reason"]=("Missing Required Field: Visit Reason")

    return errors

def validate_vitals(data):
    errors = {}

    def to_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    def to_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    visit = data.get("visit_id")

    height = to_int(data.get("height"))
    weight = to_float(data.get("weight"))
    sys = to_int(data.get("systolic"))
    dia = to_int(data.get("diastolic"))
    temp = to_float(data.get("temperature"))
    bpm = to_int(data.get("heart_rate"))
    pain = to_int(data.get("pain_level"))
    recorded_by = (data.get("recorded_by") or "").strip()

    if not visit:
        errors["visit_id"] = "Missing required field: Visit ID"

    if not recorded_by:
        errors["recorded_by"] = "Missing required field: Recorded by"

    if height is None:
        errors["height"] = "Height must be an integer"
    elif height < 1:
        errors["height"] = "Height must be at least 1"

    if weight is None:
        errors["weight"] = "Weight must be a number"
    elif weight < 1:
        errors["weight"] = "Weight must be at least 1"

    if sys is None:
        errors["systolic"] = "Systolic must be an integer"
    elif not (1 <= sys <= 200):
        errors["systolic"] = "Systolic must be 1-200"

    if dia is None:
        errors["diastolic"] = "Diastolic must be an integer"
    elif not (1 <= dia <= 200):
        errors["diastolic"] = "Diastolic must be 1-200"

    if temp is None:
        errors["temperature"] = "Temperature must be a number"
    elif not (80 <= temp <= 150):
        errors["temperature"] = "Temperature must be 80-150"

    if bpm is None:
        errors["heart_rate"] = "Heart rate must be an integer"
    elif not (20 <= bpm <= 220):
        errors["heart_rate"] = "Heart rate must be 20-220"

    if pain is None:
        errors["pain_level"] = "Pain level must be an integer"
    elif not (0 <= pain <= 10):
        errors["pain_level"] = "Pain level must be 0-10"

    return errors

def validate_icd(data):
    errors={}
    icd=(data.get("icd_code") or "").strip()

    if not icd:
        errors["icd"]=("Missing Required Field: ICD code")

    return errors

def validate_diagnosis(data):
    errors={}
    patient_id=(data.get("patient_id") or "").strip()
    icd=(data.get("icd_code") or "").strip()
    status=(data.get("status") or "").strip()

    if not patient_id:
        errors["patient_id"]=("Missing Required Field: Patient ID")

    if not icd:
        errors["icd"]=("Missing Required Field: ICD code")

    if not status:
        errors["status"]=("Missing Required Field: Status")
    elif status.lower() not in STATUS:
        errors["status"]=("Invalid Entry: Diagnosis status is not valid")