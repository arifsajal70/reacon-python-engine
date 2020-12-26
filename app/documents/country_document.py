from mongoengine import Document, fields


class Country(Document):

    meta = {
        'collection': 'countries'
    }
