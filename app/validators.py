import re
from datetime import date

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
    errors=[]
    dob=data.get("date_of_birth")
    first_name=(data.get("first_name") or "").strip()
    last_name=(data.get("last_name") or "").strip()
    email=(data.get("email") or "").strip()
    phone_number=(data.get("phone_number") or "").strip()

    if not first_name:
        errors.append("Missing Required Field: First name")
    elif len(first_name)>50:
        errors.append("Invalid Length: First name cannot have more that 50 characters")

    if not last_name:
        errors.append("Missing Required Field: Last name")
    elif len(last_name)>50:
        errors.append("Invalid Length: Last name cannot have more that 50 characters")

    if not email and not phone_number:
        errors.append("Missing Contact Information: Patient requires at least one contact method")

    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Invalid Entry: Email address is not valid")

    if phone_number and not re.match(r"^[\d\s\-\(\)\+\.]{7,20}$", phone_number):
        errors.append("Invalid Entry: Phone number is not valid")

    if dob:
        try:
            parsed=date.fromisoformat(dob)
            if parsed > date.today():
                errors.append("Invalid Entry: Date of birth cannot be in future")
        except ValueError:
            errors.append("Invalid Entry: Date of birth is not valid")
    else:
        errors.append("Missing Required Field: Date of Birth")

    return errors

def validate_provider(data):
    errors=[]
    npi=(data.get("national_provider_identifier") or "").strip()
    first_name=(data.get("first_name") or "").strip()
    last_name=(data.get("last_name") or "").strip()
    phone_number=(data.get("phone_number") or "").strip()

    if not npi:
        errors.append("Missing Required Field: National Provider Identifier")
    elif not re.match(r"^\d{10}$", npi):
        errors.append("Invalid Length: National Provider Identifier must be 10 digits")

    if not first_name:
        errors.append("Missing Required Field: First name")
    elif len(first_name)>50:
        errors.append("Invalid Length: First name cannot have more that 50 characters")

    if not last_name:
        errors.append("Missing Required Field: Last name")
    elif len(last_name)>50:
        errors.append("Invalid Length: Last name cannot have more that 50 characters")

    if phone_number and not re.match(r"^[\d\s\-\(\)\+\.]{7,20}$", phone_number):
        errors.append("Invalid Entry: Phone number is not valid")

    return errors

def validate_provider_specialty(data):
    errors=[]
    htc=(data.get("healthcare_provider_taxonomy_code") or "").strip()

    if not htc:
        errors.append("Missing Required Field: Healthcare Provider Taxonomy Code")
    elif not re.match(r"^[a-zA-Z\d]{10}$", htc):
        errors.append("Invalid Length: Healthcare Provider Taxonomy Code must be 10 alphanumeric characters")

    return errors

def validate_state_license(data):
    errors=[]
    state=(data.get("issue_state") or "").strip()
    license=(data.get("state_license") or "").strip()

    if not state:
        errors.append("Missing Required Field: Issue State")
    elif state not in STATES:
        errors.append("Invalid Entry: Issue state is not valid")

    if not license:
        errors.append("Missing Required Field: State License")

    return errors

def validate_visit(data):
    errors=[]
    patient_id=(data.get("patient_id") or "").strip()
    npi=(data.get("npi") or "").strip()
    visit_date=(data.get("visit_date") or "").strip()
    reason=(data.get("visit_reason") or "").strip()

    if not patient_id:
        errors.append("Missing Required Field: Patient ID")

    if not npi:
        errors.append("Missing Required Field: National Provider Identifier")

    if visit_date:
        try:
            parsed=date.fromisoformat(visit_date)
            if parsed > date.today():
                errors.append("Invalid Entry: Visit date cannot be in future")
        except ValueError:
            errors.append("Invalid Entry: Visit date is not valid")
    else:
        errors.append("Missing Required Field: Date of Birth")

    if not reason:
        errors.append("Missing Required Field: Visit Reason")

    return errors

def validate_vitals(data):
    errors=[]
    visit=(data.get("visit_id") or "").strip()
    height=(data.get("height") or "").strip()
    weight=(data.get("weight") or "").strip()
    sys=(data.get("systolic") or "").strip()
    dia=(data.get("diastolic") or "").strip()
    temp=(data.get("temperature") or "").strip()
    bpm=(data.get("bmp") or "").strip()
    pain=(data.get("pain_level") or "").strip()
    recorded_by=(data.get("recorded_by") or "").strip()

    def try_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0

    def try_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    if not visit:
        errors.append("Missing Required Field: visit")

    if height:
        if not try_int(height):
            errors.append("Invalid Entry: Height is not an integer")
        elif height < 1:
            errors.append("Invalid Entry: Height must be 1 or greater inches")

    if weight:
        if not try_float(weight):
            errors.append("Invalid Entry: Height is not a float")
        elif weight < 1:
            errors.append("Invalid Entry: Height must be 1 or greater lbs")

    if sys:
        if not try_int(sys):
            errors.append("Invalid Entry: Systolic pressure is not an integer")
        elif (sys < 1 or sys > 200):
            errors.append("Invalid Entry: Systolic pressure must be between 1 and 200")

    if dia:
        if not try_int(dia):
            errors.append("Invalid Entry: Diastolic pressure is not an integer")
        elif (dia < 1 or dia > 200):
            errors.append("Invalid Entry: Diastolic pressure must be between 1 and 200")

    if temp:
        if not try_float(temp):
            errors.append("Invalid Entry: Temperature is not a float")
        elif (temp < 80 or temp > 150):
            errors.append("Invalid Entry: Temperature must be between 80 and 150")

    if bpm:
        if not try_int(bpm):
            errors.append("Invalid Entry: Heart rate is not an integer")
        elif (bpm < 20 or bpm > 220):
            errors.append("Invalid Entry: Heart rate must be between 20 and 220")
    if pain:
        if not try_int(pain):
            errors.append("Invalid Entry: Pain level is not an integer")
        elif (pain < 0 or pain > 10):
            errors.append("Invalid Entry: Pain level must be between 0 and 10")

    if not recorded_by:
        errors.append("Missing Required Field: Recorded by")

    return errors

def validate_icd(data):
    errors=[]
    icd=(data.get("icd_code") or "").strip()

    if not icd:
        errors.append("Missing Required Field: ICD code")

    return errors

def validate_diagnosis(data):
    errors=[]
    patient=(data.get("patient_id") or "").strip()
    icd=(data.get("icd_code") or "").strip()
    status=(data.get("status") or "").strip()

    if not patient:
        errors.append("Missing Required Field: Patient ID")

    if not icd:
        errors.append("Missing Required Field: ICD code")

    if not status:
        errors.append("Missing Required Field: Status")
    elif status.lower() not in STATUS:
        errors.append("Invalid Entry: Diagnosis status is not valid")