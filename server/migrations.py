from playhouse.postgres_ext import *
from models import *

class migrator:
    def create_tables(self):
        ext_db = get_db()
        ext_db.execute_sql("CREATE SCHEMA IF NOT EXISTS public")
        ext_db.create_tables([DJ, Setlist, Artist, Label, Track, Track_Setlist_Link, DJ_Setlist_Link])