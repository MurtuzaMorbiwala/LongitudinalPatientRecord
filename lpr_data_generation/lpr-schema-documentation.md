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
| reason_code | string | Reason for visit (ICD code) |
| service_provider | string | Healthcare provider organization |

## 3. Condition

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | Condition code (ICD/SNOMED) |
| clinical_status | string | Active/Resolved/etc. |
| onset_date | datetime | When condition started |
| abatement_date | datetime | When condition resolved |
| recorded_date | datetime | When condition was recorded |

## 4. Observation

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | Observation code (LOINC) |
| value | string | Observation value |
| unit | string | Unit of measurement |
| interpretation | string | High/Low/Normal |
| effective_date | datetime | When observation was made |
| status | string | Final/Preliminary/etc. |

## 5. Procedure

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| code | string | Procedure code (CPT/SNOMED) |
| performed_date | datetime | When procedure was done |
| status | string | Completed/In Progress/etc. |
| performer | string | Healthcare provider name |

## 6. MedicationRequest

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| medication_code | string | Medication code (RxNorm) |
| authored_on | datetime | When prescribed |
| dosage_instruction | string | Dosage instructions |
| status | string | Active/Completed/etc. |
| intent | string | Order/Plan/etc. |

## 7. ClinicalNote

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| encounter_id | string | Foreign Key → Encounter(id) |
| related_condition_id | string | Foreign Key → Condition(id) |
| related_procedure_id | string | Foreign Key → Procedure(id) |
| related_observation_id | string | Foreign Key → Observation(id) |
| related_medication_id | string | Foreign Key → MedicationRequest(id) |
| author | string | Note author |
| note_text | string | Note content |
| created_on | datetime | When note was created |
| note_type | string | Progress/Procedure/etc. |

## 8. CarePlan

| Column Name | Type | Description |
|-------------|------|-------------|
| id | string | Primary Key |
| patient_id | string | Foreign Key → Patient(id) |
| status | string | Active/Completed/etc. |
| intent | string | Plan/Order/etc. |
| title | string | Plan title |
| period_start | datetime | Start of care plan |
| period_end | datetime | End of care plan |

## Relationships

1. Patient Relationships:
   - Patient -[HAD_ENCOUNTER]-> Encounter
   - Patient -[HAS_CONDITION]-> Condition
   - Patient -[HAS_OBSERVATION]-> Observation
   - Patient -[UNDERWENT]-> Procedure
   - Patient -[HAS_MEDICATION]-> MedicationRequest
   - Patient -[HAS_NOTE]-> ClinicalNote
   - Patient -[HAS_CARE_PLAN]-> CarePlan

2. Event Relationships:
   - Condition -[DIAGNOSED_DURING]-> Encounter
   - Observation -[OBSERVED_DURING]-> Encounter
   - Procedure -[PERFORMED_DURING]-> Encounter
   - MedicationRequest -[PRESCRIBED_DURING]-> Encounter
   - ClinicalNote -[DOCUMENTED_DURING]-> Encounter

3. Clinical Note References:
   - ClinicalNote -[REFERENCES_CONDITION]-> Condition
   - ClinicalNote -[REFERENCES_PROCEDURE]-> Procedure
   - ClinicalNote -[REFERENCES_OBSERVATION]-> Observation
   - ClinicalNote -[REFERENCES_MEDICATION]-> MedicationRequest
