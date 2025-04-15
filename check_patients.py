from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

def check_patients():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            # Get all patients and their connected entities
            result = session.run("""
                MATCH (p:Patient)
                OPTIONAL MATCH (p)-[r]->(n)
                WITH p, type(r) as rel_type, labels(n)[0] as node_type, count(*) as count
                WITH p, collect({relation: rel_type, to: node_type, count: count}) as connections
                RETURN p.name as patient_name, connections
                ORDER BY p.name
            """)
            
            print("Patient Summary:")
            print("---------------")
            for record in result:
                print(f"\nPatient: {record['patient_name']}")
                print("Connected to:")
                for conn in record['connections']:
                    if conn['relation'] and conn['to']:
                        print(f"- {conn['count']} {conn['to']}(s) via {conn['relation']}")
            
            # Get total counts for each node type
            result = session.run("""
                CALL apoc.meta.stats()
                YIELD labels, relTypes
                RETURN labels, relTypes
            """)
            
            stats = result.single()
            if stats:
                print("\nTotal Node Counts:")
                print("----------------")
                for label, count in stats['labels'].items():
                    print(f"{label}: {count}")
                
                print("\nRelationship Types:")
                print("-----------------")
                for rel_type, count in stats['relTypes'].items():
                    print(f"{rel_type}: {count}")
    finally:
        driver.close()

if __name__ == "__main__":
    check_patients()
