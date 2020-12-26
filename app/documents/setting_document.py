# Import Mongoengine Things
from mongoengine import Document, fields

# Import Helpers
from app.helpers.formatter import setting as setting_format


class Setting(Document):
    field = fields.StringField()
    value = fields.StringField()
    type = fields.StringField(choices=['str', 'int', 'float', 'image', 'bool'])

    meta = {
        'collection': 'settings'
    }

    @classmethod
    def has_field(cls, field):
        return cls.objects(field=field).count() > 0 and True or False

    @classmethod
    def get_field(cls, field):
        return cls.has_field(field) and cls.objects(field=field).first() or None

    @classmethod
    def formatted(cls, field=None):
        if field:
            return setting_format(cls.get_field(field))
        else:
            setting_list = dict()
            for setting in Setting.objects:
                setting_list[setting.field] = setting_format(setting)
            return setting_list
