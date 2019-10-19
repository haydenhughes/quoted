from flask_restful import abort
from mongoengine import DynamicDocument, StringField, URLField, ListField, ReferenceField, DoesNotExist, QuerySet, PULL


class APIQuerySet(QuerySet):
    def get_or_404(self, **kwargs):
        try:
            return self.get(**kwargs)
        except DoesNotExist:
            abort(404, message=f'{kwargs} does not exist')


class Quote(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    quote = StringField(max_length=100, required=True, unique=True)
    character = StringField()
    themes = ListField(StringField())
    uri = URLField()


class Character(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    name = StringField(max_length=100, required=True, unique=True)
    quotes = ListField(ReferenceField('Quote', reverse_delete_rule=PULL))
    uri = URLField()


class Theme(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    theme = StringField(max_length=100, required=True, unique=True)
    quotes = ListField(ReferenceField('Quote', reverse_delete_rule=PULL))
    uri = URLField()
