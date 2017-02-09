from playhouse.postgres_ext import *

def get_db():
    return PostgresqlExtDatabase('setlistspy',
                          user='postgres',
                          password="cosmicvampire",
                          host="localhost", port=5432,
                          register_hstore=False)

class BaseExtModel(Model):
    class Meta:
        database = get_db()

class DJ(BaseExtModel):
    name = CharField(unique=True)
    url = CharField(unique=True)

class Setlist(BaseExtModel):
    dj = ForeignKeyField(DJ)
    url = CharField()
    track_ids = ArrayField() #Sorted in setlist order when setlist.multi_version = True, otherwise just an aggregate
    multi_dj = BooleanField(default = False)
    multi_version = BooleanField(default = False)
    page_mod_time = DateTimeField()

class Artist(BaseExtModel):
    name = CharField(unique=True)

class Label(BaseExtModel):
    name = CharField(unique=True)

class Track(BaseExtModel):
    __tablename__ = 'tracks'
    artist = ForeignKeyField(Artist) #DO COMPOUND FORIEGN KEY
    title = CharField()
    label = ForeignKeyField(Label, null=True)

class Track_Setlist_Link(BaseExtModel):
    track = ForeignKeyField(Track)
    setlist = ForeignKeyField(Setlist)
