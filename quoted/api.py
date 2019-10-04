import json
from flask_restful import Resource, abort
from flask import request, url_for
from mongoengine import DoesNotExist, NotUniqueError
from .models import Quote


class QuoteListAPI(Resource):
    def get(self):
        return {'quotes': json.loads(Quote.objects.to_json())}

    def post(self):
        if not request.json or 'text' not in request.json:
            abort(400, message='Does the text fild exist?')

        try:
            quote = Quote(**request.json).save()
        except NotUniqueError:
            abort(
                403, message=f'The quote "{request.json["text"]}" already exists.')
        quote.uri = url_for('quote', id=quote.id, _external=True)
        quote.save()

        return {'quote': json.loads(quote.to_json())}, 201


class QuoteAPI(Resource):
    def get(self, id):
        try:
            return {'quote': json.loads(Quote.objects.get(id=id).to_json())}
        except DoesNotExist:
            abort(404, message=f'Quote {id} does not exist')

    def put(self, id):
        if not request.json:
            abort(400)
        try:
            quote = Quote.objects.get(id=id)
        except DoesNotExist:
            abort(404, message=f'Quote {id} does not exist')

        for key, value in request.json.items():
            if value == '':
                try:
                    delattr(quote, key)
                except AttributeError:
                    pass  # Doesn't matter that it doesn't exist.
            elif 'id' in request.json or 'uri' in request.json:
                abort(403, message='Modification of the uri or id field is forbidden')
            else:
                setattr(quote, key, value)
        quote.save()

        return {'quote': json.loads(quote.to_json())}

    def delete(self, id):
        try:
            quote = Quote.objects.get(id=id)
        except DoesNotExist:
            abort(404, message=f'Quote {id} does not exist')
        quote.delete()
        return '', 204
