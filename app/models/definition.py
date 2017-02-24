from peewee import CharField
from peewee import IntegerField
from peewee import Model
from peewee import SmallIntegerField
from peewee import TextField

from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('./app/static/wn31-slim3.db')

class BaseModel(Model):
    class Meta:
        database = db

class words(BaseModel):
    """Model for the slimmed down WordNet's wordsXsensesXsynsets table view.

    This table holds:
        * the word
        * it's original WordNet wordID
        * part of speech
        * it's definition.
    """
    id = IntegerField(primary_key=True)
    wordid = IntegerField()
    pos = CharField()
    us_ipa = TextField()
    word = TextField()
    definition = TextField()
