import psycopg2
from abstract.parent import AbstractParent
from db import psql_db, neo4j_db

'''Seeds the the DJ table in Postgres and Neo4j'''
class DJSeeder(AbstractParent):
    def __init__(self, starting_url = False):
        AbstractParent.__init__(self)

    def upsert_psql(self):
        conn, cursor = psql_db.connect()
        f = open('dj.csv', 'r', newline='')
        #Copy dj.csv to temp table and then upsert de-duped values to actual table
        cursor.copy_from(f, 'tmp_dj', columns=('name', 'url'))
        conn.commit()

        query = '''INSERT INTO dj (name, url)
                   SELECT DISTINCT name, url
                   FROM tmp_dj
                   ON CONFLICT (name)
                   DO UPDATE SET name = EXCLUDED.name, url = EXCLUDED.url'''
        cursor.execute(query)
        conn.commit()

        conn.close()

    def insert_into_neo4j(self):
        driver = neo4j_db.connect()
        session = driver.session()

        session.run('''LOAD CSV FROM "file:///dj.csv" AS line
                     CREATE (:DJ { name: line[0], url:line[1] })''')
        session.close()
