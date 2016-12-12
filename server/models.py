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
    url = CharField(unique=True)
    track_order = ArrayField()
    multi_tracklist = BooleanField(default=False)
    page_mod_time = DateTimeField()
    # raw sql = INSERT INTO setlist (dj_id, url, track_order, page_mod_time) VALUES(1, 'www.sjdk.com', array[1,2,3], date '30 September 2015');

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

class DJ_Setlist_Link(BaseExtModel):
    dj = ForeignKeyField(DJ)
    setlist = ForeignKeyField(Setlist)
