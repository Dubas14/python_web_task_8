from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, BooleanField

connect(db="hw", host="mongodb+srv://usergoit:UtvsAUVvctuKW9GD@evhenii.xjlco.mongodb.net/")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "author"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True)
    is_sent = BooleanField(default=False)
    preferred_method = StringField(choices=['email', 'sms'], required=True)
