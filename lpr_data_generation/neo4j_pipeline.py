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
        SET p += $properties
        """
        properties = {k: v for k, v in patient_data.items()}
        tx.run(query, id=patient_data['id'], properties=properties)

    def create_encounter_node(self, tx, encounter_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MERGE (e:Encounter {id: $id})
        SET e += $properties
        MERGE (p)-[:HAD_ENCOUNTER]->(e)
        """
        properties = {k: v for k, v in encounter_data.items() if k not in ['patient_id']}
        tx.run(query, patient_id=encounter_data['patient_id'], 
               id=encounter_data['id'], 
               properties=properties)

    def create_condition_node(self, tx, condition_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (c:Condition {id: $id})
        SET c += $properties
        MERGE (p)-[:HAS_CONDITION]->(c)
        MERGE (c)-[:DIAGNOSED_DURING]->(e)
        """
        properties = {k: v for k, v in condition_data.items() 
                    if k not in ['patient_id', 'encounter_id']}
        tx.run(query, patient_id=condition_data['patient_id'],
               encounter_id=condition_data['encounter_id'],
               id=condition_data['id'],
               properties=properties)

    def create_observation_node(self, tx, observation_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (o:Observation {id: $id})
        SET o += $properties
        MERGE (p)-[:HAS_OBSERVATION]->(o)
        MERGE (o)-[:OBSERVED_DURING]->(e)
        """
        properties = {k: v for k, v in observation_data.items() 
                    if k not in ['patient_id', 'encounter_id']}
        tx.run(query, patient_id=observation_data['patient_id'],
               encounter_id=observation_data['encounter_id'],
               id=observation_data['id'],
               properties=properties)

    def create_procedure_node(self, tx, procedure_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (proc:Procedure {id: $id})
        SET proc += $properties
        MERGE (p)-[:UNDERWENT]->(proc)
        MERGE (proc)-[:PERFORMED_DURING]->(e)
        """
        properties = {k: v for k, v in procedure_data.items() 
                    if k not in ['patient_id', 'encounter_id']}
        tx.run(query, patient_id=procedure_data['patient_id'],
               encounter_id=procedure_data['encounter_id'],
               id=procedure_data['id'],
               properties=properties)

    def create_medication_request_node(self, tx, med_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (m:MedicationRequest {id: $id})
        SET m += $properties
        MERGE (p)-[:HAS_MEDICATION]->(m)
        MERGE (m)-[:PRESCRIBED_DURING]->(e)
        """
        properties = {k: v for k, v in med_data.items() 
                    if k not in ['patient_id', 'encounter_id']}
        tx.run(query, patient_id=med_data['patient_id'],
               encounter_id=med_data['encounter_id'],
               id=med_data['id'],
               properties=properties)

    def create_care_plan_node(self, tx, care_plan_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MERGE (cp:CarePlan {id: $id})
        SET cp += $properties
        MERGE (p)-[:HAS_CARE_PLAN]->(cp)
        """
        properties = {k: v for k, v in care_plan_data.items() 
                    if k not in ['patient_id']}
        tx.run(query, patient_id=care_plan_data['patient_id'],
               id=care_plan_data['id'],
               properties=properties)

    def create_clinical_note_node(self, tx, note_data: Dict):
        query = """
        MATCH (p:Patient {id: $patient_id})
        MATCH (e:Encounter {id: $encounter_id})
        MERGE (n:ClinicalNote {id: $id})
        SET n += $properties
        MERGE (p)-[:HAS_NOTE]->(n)
        MERGE (n)-[:DOCUMENTED_DURING]->(e)
        WITH n
        MATCH (c:Condition {id: $related_condition_id})
        WHERE $related_condition_id IS NOT NULL
        MERGE (n)-[:REFERENCES_CONDITION]->(c)
        WITH n
        MATCH (pr:Procedure {id: $related_procedure_id})
        WHERE $related_procedure_id IS NOT NULL
        MERGE (n)-[:REFERENCES_PROCEDURE]->(pr)
        WITH n
        MATCH (o:Observation {id: $related_observation_id})
        WHERE $related_observation_id IS NOT NULL
        MERGE (n)-[:REFERENCES_OBSERVATION]->(o)
        WITH n
        MATCH (m:MedicationRequest {id: $related_medication_id})
        WHERE $related_medication_id IS NOT NULL
        MERGE (n)-[:REFERENCES_MEDICATION]->(m)
        """
        properties = {k: v for k, v in note_data.items() 
                    if k not in ['patient_id', 'encounter_id', 
                               'related_condition_id', 'related_procedure_id',
                               'related_observation_id', 'related_medication_id']}
        tx.run(query, 
               patient_id=note_data['patient_id'],
               encounter_id=note_data['encounter_id'],
               id=note_data['id'],
               related_condition_id=note_data.get('related_condition_id'),
               related_procedure_id=note_data.get('related_procedure_id'),
               related_observation_id=note_data.get('related_observation_id'),
               related_medication_id=note_data.get('related_medication_id'),
               properties=properties)

    def load_patient_data(self, file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)

        with self.driver.session() as session:
            # Create Patient node
            session.execute_write(self.create_patient_node, data['Patient'])

            # Create Encounter nodes
            for encounter in data['Encounters']:
                session.execute_write(self.create_encounter_node, encounter)

            # Create Condition nodes
            if 'Conditions' in data:
                for condition in data['Conditions']:
                    session.execute_write(self.create_condition_node, condition)

            # Create Observation nodes
            if 'Observations' in data:
                for observation in data['Observations']:
                    session.execute_write(self.create_observation_node, observation)

            # Create Procedure nodes
            if 'Procedures' in data:
                for procedure in data['Procedures']:
                    session.execute_write(self.create_procedure_node, procedure)

            # Create MedicationRequest nodes
            if 'MedicationRequests' in data:
                for med_request in data['MedicationRequests']:
                    session.execute_write(self.create_medication_request_node, med_request)

            # Create CarePlan nodes
            if 'CarePlans' in data:
                for care_plan in data['CarePlans']:
                    session.execute_write(self.create_care_plan_node, care_plan)

            # Create ClinicalNote nodes (after all other entities for references)
            if 'ClinicalNotes' in data:
                for note in data['ClinicalNotes']:
                    session.execute_write(self.create_clinical_note_node, note)

def process_all_patient_files(data_dir: str):
    loader = Neo4jLoader()
    try:
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        logging.info(f"Found {len(files)} JSON files: {files}")
        
        for file_name in files:
            file_path = os.path.join(data_dir, file_name)
            logging.info(f"Processing file: {file_path}")
            try:
                loader.load_patient_data(file_path)
                logging.info(f"Successfully processed {file_name}")
            except Exception as e:
                logging.error(f"Error processing {file_name}: {str(e)}")
    finally:
        loader.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    data_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_patient_files(data_dir)
