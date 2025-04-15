from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

def verify_data():
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            # Get all node types and counts
            result = session.run("""
                CALL apoc.meta.stats()
                YIELD labels
                RETURN labels
            """)
            stats = result.single()
            if stats:
                print("Node types and counts:")
                for label, count in stats['labels'].items():
                    print(f"{label}: {count}")
                
                # Get sample of each type
                node_types = list(stats['labels'].keys())
                for node_type in node_types:
                    print(f"\nSample {node_type}:")
                    result = session.run(f"""
                        MATCH (n:{node_type})
                        RETURN n LIMIT 1
                    """)
                    sample = result.single()
                    if sample:
                        print(dict(sample['n']))
    finally:
        driver.close()

if __name__ == "__main__":
    verify_data()
