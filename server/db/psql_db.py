import json
import os
import psycopg2

class PsqlHandler():
    def __init__(self):
        return

    def connect(self):
        conf = json.load(open("db/psql.json"))
        self.conn = psycopg2.connect(database=conf['database'], user=conf['username'], password=conf['password'], host=conf['host'])
        self.cursor = self.conn.cursor()

    def close_and_commit(self):
        self.conn.commit()
        self.conn.close()

    def import_all_csv(self):
        self.import_dj_csv()
        self.import_setlist_csv()

    def import_dj_csv(self):
        #Copy dj_import.csv to temp table and then upsert de-duped values to actual table
        self.connect()
        query = "TRUNCATE tmp_dj"
        self.cursor.execute(query)
        self.conn.commit()
        os.chdir('csv')
        f = open('dj_import.csv', 'r', newline='')
        self.cursor.copy_from(f, 'tmp_dj', columns=('name', 'url'))
        self.conn.commit()
        query = '''INSERT INTO dj (name, url)
                   SELECT DISTINCT name, url
                   FROM tmp_dj
                   ON CONFLICT (name)
                   DO UPDATE SET name = EXCLUDED.name, url = EXCLUDED.url'''
        self.cursor.execute(query)
        os.chdir('../')
        self.close_and_commit()

    def import_setlist_csv(self):
        #Copy setlist_import.csv to temp table and then upsert de-duped values to actual table
        self.connect()
        query = "TRUNCATE tmp_setlist"
        self.cursor.execute(query)
        self.conn.commit()
        os.chdir('csv')
        f = open('setlist_import.csv', 'r', newline='')
        self.cursor.copy_from(f, 'tmp_setlist', columns=('dj_id', 'url', 'page_mod_time'))
        self.conn.commit()
        query = '''INSERT INTO setlist (dj_id, url, page_mod_time)
                   SELECT DISTINCT dj_id, url, page_mod_time
                   FROM tmp_setlist
                '''
        self.cursor.execute(query)
        os.chdir('../')
        self.close_and_commit()

    def export_csv(self):
        tables = ["dj", "setlist"] #, "artist", "label", "track", "track_setlist_link"]
        for table in tables:
            with open(table + "_export.csv", 'w') as f:
                sql = "COPY " + table + " TO STDOUT WITH CSV HEADER"
                cur.copy_expert(sql, f)
            conn.close()
