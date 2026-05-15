DROP TABLE IF EXISTS icd;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS vitals;
DROP TABLE IF EXISTS visit;
DROP TABLE IF EXISTS providerStateLicense;
DROP TABLE IF EXISTS providerSpecialty;
DROP TABLE IF EXISTS provider;
DROP TABLE IF EXISTS patient;

CREATE TABLE icd (
    icd_code VARCHAR(20) PRIMARY KEY,
    description TEXT
);

CREATE TABLE patient (
    patient_id INTEGER PRIMARY KEY,
    patient_num VARCHAR(20) UNIQUE,
    date_of_birth DATE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE provider (
    national_provider_identifier VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE providerSpecialty (
    national_provider_identifier VARCHAR(10) NOT NULL,
    healthcare_provider_taxonomy_code VARCHAR(10) NOT NULL,
    PRIMARY KEY (national_provider_identifier, healthcare_provider_taxonomy_code),
    CONSTRAINT fk_providerspecialty_provider FOREIGN KEY (national_provider_identifier) REFERENCES provider (national_provider_identifier)
);

CREATE TABLE providerStateLicense (
    issue_state VARCHAR(25) NOT NULL,
    national_provider_identifier VARCHAR(10) NOT NULL,
    state_license VARCHAR(20) NOT NULL,
    PRIMARY KEY (issue_state, national_provider_identifier),
    CONSTRAINT fk_providerstate_provider FOREIGN KEY (national_provider_identifier) REFERENCES provider (national_provider_identifier)
);

CREATE TABLE visit (
    visit_id INTEGER PRIMARY KEY,
    visit_num VARCHAR(20) UNIQUE,
    patient_id INTEGER NOT NULL,
    national_provider_identifier VARCHAR(10) NOT NULL,
    visit_date DATETIME,
    visit_reason TEXT,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_visit_patient FOREIGN KEY (patient_id) REFERENCES patient (patient_id),
    CONSTRAINT fk_visit_provider FOREIGN KEY (national_provider_identifier) REFERENCES provider (national_provider_identifier)
);

CREATE TABLE vitals (
    vitals_id INTEGER PRIMARY KEY,
    vitals_num VARCHAR(20) UNIQUE,
    visit_id INTEGER NOT NULL,
    height INT,
    weight FLOAT,
    systolic INT,
    diastolic INT,
    temperature FLOAT,
    heart_rate INT,
    pain_level INT CHECK (pain_level BETWEEN 0 AND 10),
    recorded_by VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vitals_visit FOREIGN KEY (visit_id) REFERENCES visit (visit_id)
);

CREATE TABLE diagnosis (
    diagnosis_id INTEGER PRIMARY KEY,
    diagnosis_num VARCHAR(20) UNIQUE,
    patient_id INTEGER NOT NULL,
    icd_code VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_diagnosis_patient FOREIGN KEY (patient_id) REFERENCES patient (patient_id),
    CONSTRAINT fk_diagnosis_icd FOREIGN KEY (icd_code) REFERENCES icd (icd_code)
);