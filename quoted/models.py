from flask_restful import abort
from mongoengine import DynamicDocument, StringField, URLField, ListField, ReferenceField, DoesNotExist, QuerySet


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
    uri = URLField()


