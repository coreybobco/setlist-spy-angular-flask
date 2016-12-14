from models import *
from crawler.djs import *

class migrator:
    def __init__(self):
        self.db = get_db()
        self.models = [DJ, Setlist, Artist, Label, Track, Track_Setlist_Link, DJ_Setlist_Link]

    def initialize_db(self, drop_tables=False):
        if drop_tables:
            self.db.drop_tables(self.models)
        self.fill_schema()
        self.create_functions()

    def seed_db(self, drop_tables = False, starting_url = False):
        self.initialize_db(drop_tables)
        seeder = DJsCrawler(starting_url, True, True)
        seeder.crawl_categories_pages()

    def fill_schema(self):
        self.db.execute_sql("CREATE SCHEMA IF NOT EXISTS public")
        self.db.create_tables(self.models, safe=True)

    def create_functions(self):
        array_distinct_sql = "CREATE OR REPLACE FUNCTION array_distinct(anyarray) RETURNS anyarray AS $f$ SELECT array_agg(DISTINCT x) FROM unnest($1) t(x); $f$ LANGUAGE SQL IMMUTABLE;"
        self.db.execute_sql(array_distinct_sql)