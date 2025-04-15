from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

def show_patient_data():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            # Get patient info and related data
            result = session.run("""
                MATCH (p:Patient)
                OPTIONAL MATCH (p)-[r]->(n)
                WITH p, type(r) as rel_type, labels(n)[0] as node_type, count(*) as count
                RETURN p.name as patient_name, 
                       collect({relation: rel_type, to: node_type, count: count}) as connections
            """)
            
            for record in result:
                print(f"\nPatient: {record['patient_name']}")
                print("Connected to:")
                for conn in record['connections']:
                    if conn['relation'] and conn['to']:
                        print(f"- {conn['count']} {conn['to']}(s) via {conn['relation']}")
            
            # Get a sample of each type of node with its properties
            node_types = ['Patient', 'Encounter', 'Condition', 'Observation', 'Procedure', 'MedicationRequest', 'ClinicalNote']
            for node_type in node_types:
                print(f"\nSample {node_type}:")
                result = session.run(f"""
                    MATCH (n:{node_type})
                    RETURN n LIMIT 1
                """)
                sample = result.single()
                if sample:
                    node_data = dict(sample['n'])
                    # Format datetime objects for better readability
                    for key, value in node_data.items():
                        if str(type(value)).find('DateTime') != -1:
                            node_data[key] = str(value)
                    print(node_data)
    finally:
        driver.close()

if __name__ == "__main__":
    show_patient_data()
