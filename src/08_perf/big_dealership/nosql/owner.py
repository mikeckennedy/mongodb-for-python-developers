from datetime import datetime

import mongoengine


class Owner(mongoengine.Document):
    # show off required (not available in mongo or pymongo directly)
    name = mongoengine.StringField(required=True)

    # show off default
    created = mongoengine.DateTimeField(default=datetime.now)

    # allows us to use $set and $inc
    number_of_visits = mongoengine.IntField(default=0)

    # show off many-to-many modeling with one sided list field
    # cars can have multiple owners and an owner can own multiple cares
    car_ids = mongoengine.ListField(mongoengine.ObjectIdField())

    meta = {
        'db_alias': 'core',
        'collection': 'owners',
        'indexes': [
            'name',
            'car_ids'
        ]
    }
