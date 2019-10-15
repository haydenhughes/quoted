from mongoengine import DynamicDocument, StringField, URLField


class Quote(DynamicDocument):
    quote = StringField(max_length=100, required=True, unique=True)
    uri = URLField()
