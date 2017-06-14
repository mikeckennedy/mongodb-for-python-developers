import mongoengine
import datetime


class ServiceHistory(mongoengine.EmbeddedDocument):
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    description = mongoengine.StringField()
    price = mongoengine.FloatField()
    customer_rating = mongoengine.IntField(min_value=1, max_value=5)

