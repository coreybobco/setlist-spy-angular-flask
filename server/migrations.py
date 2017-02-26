from models import *
from crawler.dj import *
import json
import psycopg2
from db import neo4j_db
from db.psql_db import PsqlHandler

class migrator:
    def __init__(self):
        self.db = get_db()
        self.models = [DJ, Tmp_DJ, Setlist, Tmp_Setlist, Artist, Label, Track, Track_Setlist_Link]

    def initialize_db(self, drop_tables=False):
        if drop_tables:
            neo4j_db.wipe()
        self.fill_schema()

    def execute_on_all_tables(self, query):
        p = PsqlHandler()
        p.connect()
        p.cursor.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        tables = p.cursor.fetchall()
        for table in tables:
            print(query)
            p.cursor.execute("drop table " + table[1] + " cascade")
        p.close_and_commit()

    def drop_ptables(self):
        self.execute_on_all("drop table {0} cascade")

    def truncate_ptables(self):
        self.execute_on_all("truncate table {0}")

    def fill_schema(self):
        self.db.execute_sql("CREATE SCHEMA IF NOT EXISTS public")
        self.db.create_tables(self.models, safe=True)
