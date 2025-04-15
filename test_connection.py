from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

def test_connection():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            # Count nodes by type
            result = session.run("""
                MATCH (n) 
                RETURN labels(n) as type, count(n) as count
                ORDER BY type
            """)
            print("Node counts by type:")
            for record in result:
                print(f"{record['type']}: {record['count']}")
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->() 
                RETURN type(r) as type, count(r) as count
                ORDER BY type
            """)
            print("\nRelationship counts by type:")
            for record in result:
                print(f"{record['type']}: {record['count']}")
            
            # Sample patient data
            result = session.run("""
                MATCH (p:Patient)
                RETURN p.name as name, p.gender as gender
                LIMIT 3
            """)
            print("\nSample patients:")
            for record in result:
                print(f"Name: {record['name']}, Gender: {record['gender']}")
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()
