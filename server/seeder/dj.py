import csv
import psycopg2
import time
from abstract.parent import AbstractParent
import db

'''Seeds the the DJ table in Postgres'''
class DJSeeder(AbstractParent):
    def __init__(self, starting_url = False):
        AbstractParent.__init__(self)

    def upsert(self):
        f = open('dj.csv', 'r', newline='')
        conn, cursor = db.connect()
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
