import psycopg2
from abstract.parent import AbstractParent
from db import psql_db, neo4j_db

class SetlistSeeder(AbstractParent):
    def __init__(self):
        AbstractParent.__init__(self)

    def upsert_into_psql(self):
        conn, cursor = psql_db.connect()
        f = open('setlist.csv', 'r', newline='')
        #Copy dj.csv to temp table and then upsert de-duped values to actual table
        cursor.copy_from(f, 'tmp_setlist', columns=('dj', 'url', 'page_mod_time'))
        conn.commit()

        query = '''INSERT INTO setlist (name, url)
                   SELECT DISTINCT dj, url, page_mod_time
                   FROM tmp_setlist
                '''
        cursor.execute(query)
        conn.commit()
        conn.close()

    def upsert_into_neo4j(self):
        driver = neo4j_db.connect()
        session = driver.session()

        session.run('''LOAD CSV FROM "file:///setlist.csv" AS line
                     CREATE (:DJ { name: line[0], url:line[1] })''')
        session.close()
