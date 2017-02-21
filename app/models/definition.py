from peewee import *
from peewee import CharField
from peewee import TextField
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('./app/static/sqlite-31_snapshot.db')

class BaseModel(Model):
    class Meta:
        database = db

class wordsXsensesXsynsets(BaseModel):
    wordid = IntegerField(primary_key=True)
    lemma = CharField()
    casedwordid = IntegerField()
    synsetid = IntegerField()
    senseid = IntegerField()
    sensenum =  SmallIntegerField()
    lexid =  SmallIntegerField()
    tagcount = IntegerField()
    sensekey = TextField()
    pos = CharField()
    lexdomainid =  SmallIntegerField()
    definition = TextField()
