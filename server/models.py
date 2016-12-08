from peewee import *
from playhouse.postgres_ext import *

ext_db = PostgresqlExtDatabase('setlistspy', user='postgres', password="cosmicvampire", host="localhost", port=5432, register_hstore=False)

class BaseExtModel(Model):
    class Meta:
        database = ext_db

class DJ(BaseExtModel):
    name = CharField(unique=True)

class Setlist(BaseExtModel):
    dj = ForeignKeyField(DJ)
    url = CharField(unique=True)
    order = ArrayField()
    page_mod_time = DateTimeField()

class Artist(BaseExtModel):
    name = CharField(unique=True)

class Label(BaseExtModel):
    name = CharField(unique=True)

class Track(BaseExtModel):
    __tablename__ = 'tracks'
    artist = ForeignKeyField(Artist)
    title = CharField()
    label = ForeignKeyField(Label)

class Track_Setlist_Link(BaseExtModel):
    track = ForeignKeyField(Track)
    setlist = ForeignKeyField(Setlist)

ext_db.connect()
ext_db.create_tables([DJ, Setlist, Artist, Label, Track, Track_Setlist_Link])