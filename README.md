# Longitudinal Patient Record Knowledge Graph

This project creates a knowledge graph representation of longitudinal patient records using Neo4j. It processes patient data from JSON files and builds a comprehensive graph database that captures the relationships between patients, their encounters, conditions, observations, procedures, medications, and clinical notes.

## Project Structure

```
├── lpr_data_generation/      # Patient data and processing scripts
│   ├── *.json               # Patient data files
│   └── neo4j_pipeline.py    # Main pipeline for loading data into Neo4j
├── dags/                    # Airflow DAG definitions
│   └── lpr_to_neo4j_dag.py # DAG for scheduling data loads
├── requirements.txt         # Python dependencies
└── .env                    # Environment variables (not in version control)
```

## Features

- Comprehensive patient data model including:
  - Patient demographics
  - Medical encounters
  - Health conditions
  - Clinical observations
  - Medical procedures
  - Medication requests
  - Clinical notes

- Rich relationships between entities:
  - Patient → Encounters (HAD_ENCOUNTER)
  - Patient → Conditions (HAS_CONDITION)
  - Patient → Observations (HAS_OBSERVATION)
  - Patient → Procedures (UNDERWENT)
  - Patient → Medications (HAS_MEDICATION)
  - Patient → Clinical Notes (HAS_NOTE)
  - Secondary relationships (e.g., PERFORMED_DURING, DIAGNOSED_DURING)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/MurtuzaMorbiwala/LongitudinalPatientRecord.git
cd LongitudinalPatientRecord
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.template` to `.env`
   - Update Neo4j credentials in `.env`:
```
NEO4J_URI=neo4j+s://<your-instance-id>.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

## Usage

### One-time Data Load

To load all patient data into Neo4j:

```bash
python clear_and_load.py
```

### Scheduled Data Load with Airflow

1. Place the DAG file in your Airflow dags folder:
```bash
cp dags/lpr_to_neo4j_dag.py $AIRFLOW_HOME/dags/
```

2. The DAG will run daily to load any new or updated patient data.

### Verifying Data

To check the loaded data:

```bash
python check_patients.py
```

This will show:
- Number of nodes by type
- Number of relationships by type
- Sample data for each patient

## Data Model

### Node Types
- Patient: Core patient demographics
- Encounter: Healthcare visits and interactions
- Condition: Health conditions and diagnoses
- Observation: Clinical measurements and findings
- Procedure: Medical procedures performed
- MedicationRequest: Prescribed medications
- ClinicalNote: Healthcare provider notes

### Relationship Types
- HAD_ENCOUNTER: Patient to Encounter
- HAS_CONDITION: Patient to Condition
- HAS_OBSERVATION: Patient to Observation
- UNDERWENT: Patient to Procedure
- HAS_MEDICATION: Patient to MedicationRequest
- HAS_NOTE: Patient to ClinicalNote
- PERFORMED_DURING: Procedure to Encounter
- DIAGNOSED_DURING: Condition to Encounter
- OBSERVED_DURING: Observation to Encounter
- PRESCRIBED_DURING: MedicationRequest to Encounter
- DOCUMENTED_DURING: ClinicalNote to Encounter

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
