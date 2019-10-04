from mongoengine import DynamicDocument, StringField, URLField


class Quote(DynamicDocument):
    text = StringField(max_length=20, required=True, unique=True)
    uri = URLField()
