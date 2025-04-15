from neo4j import GraphDatabase
import json
import os
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Neo4jLoader:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_patient_node(self, tx, patient_data: Dict):
        query = """
        MERGE (p:Patient {id: $id})
        SET p.identifier = $identifier,
            p.name = $name,
            p.gender = $gender,
            p.birth_date = $birth_date,
            p.address = $address,
            p.telecom = $telecom,
            p.managing_organization = $managing_organization
        """
        tx.run(query, **patient_data)

    def create_encounter_node(self, tx, encounter_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MERGE (e:Encounter {id: $id})
        SET e.status = $status,
            e.class = $class,
            e.type = $type,
            e.period_start = datetime($period_start),
            e.period_end = datetime($period_end),
            e.reason_code = $reason_code,
            e.service_provider = $service_provider
        MERGE (p)-[:HAD_ENCOUNTER]->(e)
        """
        tx.run(query, **encounter_data)

    def create_procedure_node(self, tx, procedure_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (proc:Procedure {id: $id})
        SET proc.code = $code,
            proc.name = $name,
            proc.status = $status,
            proc.performed_date = datetime($performed_date)
        MERGE (p)-[:UNDERWENT]->(proc)
        MERGE (proc)-[:PERFORMED_DURING]->(e)
        """
        tx.run(query, **procedure_data)

    def create_clinical_note_node(self, tx, note_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (n:ClinicalNote {id: $id})
        SET n.text = $text,
            n.date = datetime($date),
            n.author = $author,
            n.type = $type
        MERGE (p)-[:HAS_NOTE]->(n)
        MERGE (n)-[:DOCUMENTED_DURING]->(e)
        """
        tx.run(query, **note_data)

    def load_patient_data(self, file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        with self.driver.session() as session:
            # Create Patient node
            session.execute_write(self.create_patient_node, data['Patient'])

            # Create Encounter nodes
            for encounter in data['Encounters']:
                session.execute_write(self.create_encounter_node, encounter)

            # Create Procedure nodes
            for procedure in data['Procedures']:
                session.execute_write(self.create_procedure_node, procedure)

            # Create ClinicalNote nodes
            for note in data['ClinicalNotes']:
                session.execute_write(self.create_clinical_note_node, note)

def process_all_patient_files(data_dir: str):
    loader = Neo4jLoader()
    try:
        for file_name in os.listdir(data_dir):
            if file_name.endswith('-lpr.json'):
                file_path = os.path.join(data_dir, file_name)
                logging.info(f"Processing file: {file_path}")
                loader.load_patient_data(file_path)
    finally:
        loader.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_patient_files(data_dir)
