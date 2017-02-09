from models import *
from crawler.dj_categories import *
import json
import psycopg2
import sys

class migrator:
    def __init__(self):
        self.db = get_db()
        # self.models = [DJ, Setlist, Artist, Label, Track, Track_Setlist_Link]

    def initialize_db(self, drop_tables=False):
        if drop_tables:
            self.db.drop_tables(self.models)
        self.fill_schema()
        self.create_functions()

    def seed_db(self, drop_tables = False, starting_url = False):
        self.initialize_db(drop_tables)
        seeder = DJCategoriesCrawler(starting_url, True)
        seeder.crawl_categories_pages()

    def fill_schema(self):
        self.db.execute_sql("CREATE SCHEMA IF NOT EXISTS public")
        self.db.create_tables(self.models, safe=True)

    def create_functions(self):
        array_distinct_sql = "CREATE OR REPLACE FUNCTION array_distinct(anyarray) RETURNS anyarray AS $f$ SELECT array_agg(DISTINCT x) FROM unnest($1) t(x); $f$ LANGUAGE SQL IMMUTABLE;"
        self.db.execute_sql(array_distinct_sql)

    def copy_tables_to_csv(self):
        db = json.load(open("db.json"))
        conn = psycopg2.connect(database=db['database'], user=db['username'], password=db['password'], host=db['host'])
        self.cur = conn.cursor()
        tables = ["dj", "setlist", "artist", "label", "track", "track_setlist_link"]
        for table in tables:
            with open(table + ".csv", 'w') as f:
                sql = "COPY " + table + " TO STDOUT WITH CSV HEADER"
                cur.copy_expert(sql, f)
            conn.close()
