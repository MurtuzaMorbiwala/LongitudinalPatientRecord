from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from lpr_data_generation.neo4j_pipeline import process_all_patient_files
import logging

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

def clear_database():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        logging.info("Clearing existing data...")
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()

def main():
    # Clear existing data
    clear_database()
    
    # Load new data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lpr_data_generation')
    logging.info(f"Loading data from {data_dir}")
    process_all_patient_files(data_dir)
    
    # Print summary
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            WITH labels(n) as type, count(n) as count
            RETURN type, count
            ORDER BY type
        """)
        print("\nNode counts by type:")
        for record in result:
            print(f"{record['type']}: {record['count']}")
            
        result = session.run("""
            MATCH ()-[r]->()
            WITH type(r) as type, count(r) as count
            RETURN type, count
            ORDER BY type
        """)
        print("\nRelationship counts by type:")
        for record in result:
            print(f"{record['type']}: {record['count']}")
    driver.close()

if __name__ == "__main__":
    main()
