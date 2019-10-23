from flask_restful import abort
from flask import url_for
from mongoengine import DynamicDocument, StringField, URLField, ListField, ReferenceField, DoesNotExist, QuerySet, PULL


class APIQuerySet(QuerySet):
    def get_or_404(self, **kwargs):
        try:
            return self.get(**kwargs)
        except DoesNotExist:
            abort(404)


class Quote(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    quote = StringField(required=True, unique=True)
    character = StringField()
    significance = StringField()
    themes = ListField(StringField())
    uri = URLField()

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if Character.objects(name=document.character).count() == 0:
            (character := Character(name=document.character)).save()
            character.uri = url_for(
                'character', id=character.id, _external=True)
            character.save()
        else:
            # Call save function to update the quotes list
            Character.objects.get(name=document.character).save()

        for theme in document.themes:
            if Theme.objects(theme=theme).count() == 0:
                (theme := Theme(theme=theme)).save()
                theme.uri = url_for(
                    'theme', id=character.id, _external=True)
                theme.save()
            else:
                # Call save function to update the quotes list
                Theme.objects.get(theme=theme).save()


class Character(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    name = StringField(max_length=100, required=True, unique=True)
    quotes = ListField(ReferenceField('Quote', reverse_delete_rule=PULL))
    uri = URLField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.quotes = [
            quote for quote in Quote.objects(character=document.name)]


class Theme(DynamicDocument):
    meta = {'queryset_class': APIQuerySet}
    theme = StringField(required=True, unique=True)
    quotes = ListField(ReferenceField('Quote', reverse_delete_rule=PULL))
    uri = URLField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.quotes = [
            quote for quote in Quote.objects(themes=document.theme)]
