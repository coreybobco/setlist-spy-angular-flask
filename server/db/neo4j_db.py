from neo4j.v1 import GraphDatabase, basic_auth, TRUST_ALL_CERTIFICATES

def connect():
    uri = "bolt://localhost:7687"
    auth_token = basic_auth("pyneo", "pyneo")
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("pyneo", "pyneo"))
    return driver

def wipe():
    driver = connect()
    session = driver.session()
    query = '''MATCH (n)
            OPTIONAL MATCH (n)-[r]-()
            WITH n,r LIMIT 50000
            DELETE n,r
            RETURN count(n) as deletedNodesCount'''
    session.run(query)
    session.close()
