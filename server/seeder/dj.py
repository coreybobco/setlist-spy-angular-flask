import psycopg2
from abstract.parent import AbstractParent
from db import psql_db, neo4j_db

'''Seeds the the DJ table in Postgres and Neo4j'''
class DJSeeder(AbstractParent):
    def __init__(self):
        AbstractParent.__init__(self)

    def upsert_into_neo4j(self):
        driver = neo4j_db.connect()
        session = driver.session()

        session.run('''LOAD CSV FROM "file:///dj.csv" AS line
                     MERGE (:DJ { name: line[0], url:line[1] })''')
        session.close()
