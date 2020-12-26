# Import Documents
from app.documents.setting_document import Setting as SettingDocument

# Import Flask Things
from flask import jsonify


def login():
    return jsonify(SettingDocument.formatted(field='referer_type_1'))
