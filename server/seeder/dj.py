import csv
import psycopg2
import time
from seeder.abstract import AbstractSeeder

'''Seeds the the DJ table in Postgres'''
class DJSeeder(AbstractSeeder):
    def __init__(self, starting_url = False):
        AbstractSeeder.__init__(self)

    def upsert(self):
        f = open('dj.csv', 'r', newline='')
        conn = psycopg2.connect(database=self.db['database'], user=self.db['username'], password=self.db['password'], host=self.db['host'])
        cursor = conn.cursor()
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
