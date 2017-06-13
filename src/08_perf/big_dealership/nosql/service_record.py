import datetime
import mongoengine


class ServiceRecord(mongoengine.EmbeddedDocument):
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    description = mongoengine.StringField()
    price = mongoengine.FloatField(required=True)
    customer_rating = mongoengine.IntField(required=True)  # 1 - 5 satisfaction level.
