from playhouse.postgres_ext import *

def get_db():
    return PostgresqlExtDatabase('setlistspy_test',
                          user='ft_marinetti',
                          password="1000xenomorphs!!!",
                          host="localhost", port=5432,
                          register_hstore=False)

class BaseExtModel(Model):
    class Meta:
        database = get_db()

class DJ(BaseExtModel):
    name = CharField(unique=True)
    url = CharField(unique=True)

class Tmp_DJ(BaseExtModel):
    name = CharField()
    url = CharField()

class Setlist(BaseExtModel):
    dj = ForeignKeyField(DJ)
    url = CharField()
    page_mod_time = DateTimeField()
    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('dj', 'url'), True),
        )

class Tmp_Setlist(BaseExtModel):
    dj = ForeignKeyField(DJ)
    url = CharField()
    page_mod_time = DateTimeField()

class Artist(BaseExtModel):
    name = CharField(unique=True)

class Label(BaseExtModel):
    name = CharField(unique=True)

class Track(BaseExtModel):
    artist = ForeignKeyField(Artist)
    title = CharField()
    label = ForeignKeyField(Label, null=True)
    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('artist', 'title'), True),
        )

class Track_Setlist_Link(BaseExtModel):
    track = ForeignKeyField(Track)
    setlist = ForeignKeyField(Setlist)
    set_order_id = IntegerField()
