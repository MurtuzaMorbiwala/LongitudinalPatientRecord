# LPR Schema Documentation

## 1. Patient

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key (Patient.id) |
| identifier | string | MRN / National ID |
| name | string | Full name |
| gender | string | Male / Female / Other |
| birth_date | date | Date of birth |
| address | string | Address |
| telecom | string | Phone/email |
| managing_organization | string | Organization managing patient |

## 2. Encounter

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| status | string | Encounter status |
| class | string | Encounter type (inpatient, etc.) |
| type | string | Visit type (ER, follow-up, etc.) |
| period_start | datetime | Start date/time |
| period_end | datetime | End date/time |
| reason_code | string | Reason for visit |
| service_provider | string | Organization |

## 3. Condition

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | Diagnosis code (ICD-10/SNOMED) |
| clinical_status | string | Active / Resolved |
| onset_date | datetime | When condition began |
| abatement_date | datetime | When condition ended (if resolved) |
| recorded_date | datetime | Date of recording |

## 4. Observation

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | LOINC code (e.g., BP, glucose) |
| value | string | Measurement value |
| unit | string | Unit of measure |
| interpretation | string | Normal, abnormal, etc. |
| effective_date | datetime | Date/time of observation |
| status | string | Final, amended, etc. |

## 5. Procedure

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | CPT/SNOMED code |
| performed_date | datetime | Date/time of procedure |
| status | string | Completed / In-progress |
| performer | string | Practitioner or organization |

## 6. MedicationRequest

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| medication_code | string | RxNorm or custom code |
| authored_on | datetime | When prescribed |
| dosage_instruction | string | Dosage info |
| status | string | Active / Completed |
| intent | string | Order / Plan |

## 7. CarePlan

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| status | string | Active / Completed |
| intent | string | Plan / Order / Option |
| title | string | Care plan title |
| period_start | datetime | Start date |
| period_end | datetime | End date |

## 8. ClinicalNote

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | (optional) FK → Encounter(id) |
| related_condition_id | string | (optional) FK → Condition(id) |
| related_procedure_id | string | (optional) FK → Procedure(id) |
| related_observation_id | string | (optional) FK → Observation(id) |
| related_medication_id | string | (optional) FK → MedicationRequest(id) |
| author | string | Who wrote the note |
| note_text | text | Full unstructured text |
| created_on | datetime | When the note was created |
| note_type | string | E.g., progress note, discharge summary, etc. |
