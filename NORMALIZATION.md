# Normalization Audit Report

This report provides an analysis for the relational database for the healthcare charting application. The goal is to create and maintain a database in Boyce-Codd Normal Form (BCNF).

## Table of Contents

- [Normalization Audit Report](#normalization-audit-report)
  - [Table of Contents](#table-of-contents)
  - [patient](#patient)
    - [patient Original Table](#patient-original-table)
    - [patient Table Functional Dependencies](#patient-table-functional-dependencies)
    - [patient Anomalies](#patient-anomalies)
    - [patient Decomposition](#patient-decomposition)
  - [provider](#provider)
    - [provider Original Table](#provider-original-table)
    - [provider Table Functional dependencies](#provider-table-functional-dependencies)
    - [provider Anomalies](#provider-anomalies)
    - [provider Decomposition](#provider-decomposition)
  - [visit](#visit)
    - [visit Original Table](#visit-original-table)
    - [visit Table Functional dependencies](#visit-table-functional-dependencies)
    - [visit Anomalies](#visit-anomalies)
    - [visit Decomposition](#visit-decomposition)
  - [vitals](#vitals)
    - [vitals Original Table](#vitals-original-table)
    - [vitals Table Functional dependencies](#vitals-table-functional-dependencies)
    - [vitals Anomalies](#vitals-anomalies)
    - [vitals Decomposition](#vitals-decomposition)
  - [diagnosis](#diagnosis)
    - [diagnosis Original Table](#diagnosis-original-table)
    - [diagnosis Table Functional dependencies](#diagnosis-table-functional-dependencies)
    - [diagnosis Anomalies](#diagnosis-anomalies)
    - [diagnosis Decomposition](#diagnosis-decomposition)
  - [Final Schema](#final-schema)

## patient

### patient Original Table

| Column | Type | Constraints |
| --- | --- | --- |
| patient_id | VARCHAR(20) | PRIMARY KEY |
| date_of_birth | DATE | NOT NULL |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | |
| phone_number | VARCHAR(20) | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

### patient Table Functional Dependencies

- patient_id -> date_of_birth, first_name, last_name, email, phone_number, created_at, updated_at

### patient Anomalies

- Insertion: Inserting a patient without any email or phone number could result in an inability to contact the patient
- Deletion: Deleting a patient row could result in the foreign key to patient_id in the visit table losing its relationship, creating issues with data retrieval and relationships if the deletion is not handled properly

### patient Decomposition

The original table is already in BCNF, patient_id is a superkey.

## provider

### provider Original Table

| Column | Type | Constraints |
| --- | --- | --- |
| provider_id | VARCHAR(20) | PRIMARY KEY |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| specialty | VARCHAR(25) | |
| state_license | VARCHAR(20) | NOT NULL |
| national_provider_identifier | VARCHAR(10) | NOT NULL |
| phone_number | VARCHAR(20) |  NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

### provider Table Functional dependencies

- provider_id -> first_name, last_name, specialty, state_license, national_provider_identifier, phone_number, created_at, updated_at
- national_provider_identifier -> provider_id, first_name, last_name, specialty, state_license, phone_number

### provider Anomalies

- Update: National provider identifier was not made unique so if the same provider is added to the table under different provider_ids to account for different specialties, if the NPI is updated in one row but not the other there is an inconsistency created.
- Insertion: Inserting a provider without a state license or NPI would risk allowing providers with no license to practice.
- Deletion: Deleting a provider row could result in the foreign key to provider_id in the visit table losing its relationship, creating issues with data retrieval and relationships if the deletion is not handled properly

### provider Decomposition

The original table is not in BCNF.

National provider identifier is a nationally unique identifier and so would make a better primary key rather than the provider_id. In this case, provider_id can be removed all together and national_provider_identifier can be the primary key

provider table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| specialty | VARCHAR(25) | |
| state_license | VARCHAR(20) | NOT NULL |
| phone_number | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

Specialty would be better classified by the healthcare provider taxonomy code, which are nationally unique and regulated codes for different specialties. Since each provider can have more than one specialty, it makes sense to have the provider specialty table have a composite primary key of the NPI and HPTC

provider table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| state_license | VARCHAR(20) | NOT NULL |
| phone_number | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

providerSpecialty table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY, FK: provider(national_provider_identifier) |
| healthcare_provider_taxonomy_code | VARCHAR(10) | PRIMARY KEY |

A provider will only ever have one state license in a given state but could have state licenses from different states. Additionally, states may reuse the same license number. So, issue state for the state license should be added as an attribute to clarify what state the license is from. Because the issue state is not depended on the NPI, the state license information should be moved to its own table.

provider table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| phone_number | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

The functional dependencies are now

national_provider_identifier -> first_name, last_name, phone_number

national_provider_identifier is a superkey

providerSpecialty table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY, FK: provider(national_provider_identifier) |
| healthcare_provider_taxonomy_code | VARCHAR(10) | PRIMARY KEY |

The functional dependencies are now

national_provider_identifier, healthcare_provider_taxonomy_code -> None

national_provider_identifier and healthcare_provider_taxonomy_code together are a superkey

providerStateLicense table

| Column | Type | Constraints |
| --- | --- | --- |
| issue_state | VARCHAR(25) | PRIMARY KEY |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY, FK: provider(national_provider_identifier) |
| state_license | VARCHAR(20) | NOT NULL |

The functional dependencies are now

issue_state, national_provider_identifier -> state_license

issue_state and national_provider_identifier together are superkey

Insertion anomaly: Not able to insert a row into the state license without having a provider with a national_provider_identifier already existing.

## visit

### visit Original Table

| Column | Type | Constraints |
| --- | --- | --- |
| visit_id | VARCHAR(20) | PRIMARY KEY |
| patient_id | VARCHAR(20) | NOT NULL, FK: patient(patient_id) |
| provider_id | VARCHAR(20) | NOT NULL, FK: provider(provider_id) |
| visit_date | DATETIME | NOT NULL |
| visit_reason | TEXT | NOT NULL |
| notes | TEXT | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

### visit Table Functional dependencies

- visit_id -> patient_id, provider_id, visit_date, visit_reason, notes, created_at, updated_at

### visit Anomalies

- Update: Updating the patient_id or provider_id in the patient or provider table but not updating it in the visit table would break the foreign key relationship between the tables.
- Insertion: Inserting a visit without a patient_id and provider_id breaks the foreign key constraint and would cause issues with being able to identify who the visit was for and who it was with.
- Deletion: Deleting a row from visits affects the foreign key in both vitals and diagnosis. This could create data retrieval and relationship issues if not handles properly.

### visit Decomposition

The original table is already in BCNF, visit_id is a superkey. But because the provider table was updated to replace provider_id with national_provider_identifier as the primary key, the foreign key to provider needs to be updated.

| Column | Type | Constraints |
| --- | --- | --- |
| visit_id | VARCHAR(20) | PRIMARY KEY |
| patient_id | VARCHAR(20) | NOT NULL, FK: patient(patient_id) |
| national_provider_identifier | VARCHAR(10) | NOT NULL, FK: provider(national_provider_identifier) |
| visit_date | DATETIME | NOT NULL |
| visit_reason | TEXT | NOT NULL |
| notes | TEXT | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

visit_id -> patient_id, national_provider_identifier, visit_date, visit_reason, notes, created_at, updated_at

visit_id is still a superkey

## vitals

### vitals Original Table

| Column | Type | Constraints |
| --- | --- | --- |
| vitals_id | VARCHAR(20) | PRIMARY KEY |
| visit_id | VARCHAR(20) | NOT NULL, FK: visit(visit_id) |
| height | INT | |
| weight | FLOAT | |
| bmi | FLOAT | |
| systolic | INT | |
| diastolic | INT | |
| temperature | FLOAT | |
| heart_rate | INT | |
| pain_level | INT | CHECK (0–10) |
| recorded_by | VARCHAR(100) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

### vitals Table Functional dependencies

- vitals_id -> visit_id, height, weight, bmi, systolic, diastolic, temperature, heart_rate, pain_level, recorded_by, created_at
- height, weight -> bmi

### vitals Anomalies

- Update: If either height or weight is changed but bmi is not updated, there will be inaccurate data in the values.
- Insertion: Inserting vitals record without a visit_id breaks the foreign key constraint between the vitals and visit tables and would result in not being able to tell what patient the vitals are for. Inserting a vitals row with height and weight but no bmi.
- Deletion: Deleting a vitals row removes it's relationship to the visit table meaning a visit could lose important patient data.

### vitals Decomposition

The original table is not in BCNF.

The BMI should be taken out of the vitals table and added to a separate BMI table with height and weight as a primary key. However, this creates a lot of redundancy in data so it would be better to remove BMI and calculate it as needed.

vitals table

| Column | Type | Constraints |
| --- | --- | --- |
| vitals_id | VARCHAR(20) | PRIMARY KEY |
| visit_id | VARCHAR(20) | NOT NULL, FK: visit(visit_id) |
| height | INT | |
| weight | FLOAT | |
| systolic | INT | |
| diastolic | INT | |
| temperature | FLOAT | |
| heart_rate | INT | |
| pain_level | INT | CHECK (0–10) |
| recorded_by | VARCHAR(100) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

The functional dependencies are now

vitals_id -> visit_id, height, weight, systolic, diastolic, temperature, heart_rate, pain_level, recorded_by, created_at

vitals_id is a superkey

## diagnosis

### diagnosis Original Table

| Column | Type | Constraints |
| --- | --- | --- |
| diagnosis_id | VARCHAR(20) | PRIMARY KEY |
| visit_id | VARCHAR(20) | NOT NULL, FK: visit(visit_id) |
| icd_code | VARCHAR(20) | NOT NULL |
| description | TEXT | |
| status | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

### diagnosis Table Functional dependencies

- diagnosis_id -> visit_id, icd_code, description, status, created_at, updated_at
- icd_code -> description

### diagnosis Anomalies

- Update: Updating the description for one row and then not updating the description for another row with the same icd code would lead to inconsistencies.
- Insertion: Inserting a diagnosis with no visit_id would mean that the diagnosis will not be able to be tied to a patient or the provider that give the diagnosis.
- Deletion: Deleting all of the rows with a certain ICD would mean the loss of the information for the ICD and description

### diagnosis Decomposition

The original table is not in BCNF.

Since the description is based on the ICD, ICD and description should be pulled out into a new table with ICD as the primary key. Additionally, it makes more sense to have the diagnosis tied to the patient rather than a particular visit.

diagnosis Table

| Column | Type | Constraints |
| --- | --- | --- |
| diagnosis_id | VARCHAR(20) | PRIMARY KEY |
| patient_id | VARCHAR(20) | NOT NULL, FK: patient(patient_id) |
| icd_code | VARCHAR(20) | NOT NULL, FK: icd(icd_code |
| status | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

The functional dependencies are now

diagnosis_id -> patient_id, icd_code, status, created_at, updated_at

diagnosis_id is a superkey

icd table

| Column | Type | Constraints |
| --- | --- | --- |
| icd_code | VARCHAR(20) | PRIMARY KEY |
| description | TEXT | |

The functional dependencies are now

icd_code -> description

icd_code is a superkey

Insertion anomaly: If the icd code is inserted with no description, the tie between the two is lost. The diagnosis table cannot reference an icd code until it has been created in the icd table.

## Final Schema

patient Table

| Column | Type | Constraints |
| --- | --- | --- |
| patient_id | VARCHAR(20) | PRIMARY KEY |
| date_of_birth | DATE | NOT NULL |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | |
| phone_number | VARCHAR(20) | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

provider table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| phone_number | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

providerSpecialty table

| Column | Type | Constraints |
| --- | --- | --- |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY, FK: provider(national_provider_identifier) |
| healthcare_provider_taxonomy_code | VARCHAR(10) | PRIMARY KEY |

providerStateLicense table

| Column | Type | Constraints |
| --- | --- | --- |
| issue_state | VARCHAR(25) | PRIMARY KEY |
| national_provider_identifier | VARCHAR(10) | PRIMARY KEY, FK: provider(national_provider_identifier) |
| state_license | VARCHAR(20) | NOT NULL |

visit Table

| Column | Type | Constraints |
| --- | --- | --- |
| visit_id | VARCHAR(20) | PRIMARY KEY |
| patient_id | VARCHAR(20) | NOT NULL, FK: patient(patient_id) |
| national_provider_identifier | VARCHAR(10) | NOT NULL, FK: provider(national_provider_identifier ) |
| visit_date | DATETIME | NOT NULL |
| visit_reason | TEXT | NOT NULL |
| notes | TEXT | |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

vitals table

| Column | Type | Constraints |
| --- | --- | --- |
| vitals_id | VARCHAR(20) | PRIMARY KEY |
| visit_id | VARCHAR(20) | NOT NULL, FK: visit(visit_id) |
| height | INT | |
| weight | FLOAT | |
| systolic | INT | |
| diastolic | INT | |
| temperature | FLOAT | |
| heart_rate | INT | |
| pain_level | INT | CHECK (0–10) |
| recorded_by | VARCHAR(100) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

diagnosis Table

| Column | Type | Constraints |
| --- | --- | --- |
| diagnosis_id | VARCHAR(20) | PRIMARY KEY |
| patient_id | VARCHAR(20) | NOT NULL, FK: patient(patient_id) |
| icd_code | VARCHAR(20) | NOT NULL, FK: icd(icd_code |
| status | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

icd table

| Column | Type | Constraints |
| --- | --- | --- |
| icd_code | VARCHAR(20) | PRIMARY KEY |
| description | TEXT | |
