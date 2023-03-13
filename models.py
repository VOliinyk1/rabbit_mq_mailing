from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Users(Document):
    name = StringField()
    email = StringField()
    is_mailed = BooleanField(default=False)
