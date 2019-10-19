import json
from flask_restful import Resource, abort
from flask import request, url_for
from mongoengine import NotUniqueError, ValidationError
from .models import Quote, Character


class QuoteListAPI(Resource):
    def get(self):
        return {'quotes': json.loads(Quote.objects.to_json())}

    def post(self):
        if not request.json or 'quote' not in request.json or 'id' in request.json or 'uri' in request.json:
            abort(403, message='Does the text field exist?')

        try:
            quote = Quote(**request.json).save()
        except NotUniqueError:
            abort(
                403, message=f'The quote "{request.json["quote"]}" already exists.')
        except ValidationError as e:
            abort(403, message=e)

        quote.uri = url_for('quote', id=quote.id, _external=True)
        quote.save()

        if quote.character is not None:
            # Check to see if the character of the quote already exists then
            # append the new quote to it's quote list, otherwise create a new
            # character.

            # uncomment when python3.8 is mainstream
            # if (character := Character.objects(name=quote.character)).count() > 0:

            # TODO: remove me when migrated to python3.8
            if Character.objects(name=quote.character).count() > 0:
                # TODO: remove me when migrated to python3.8
                character = Character.objects.get(name=quote.character)
                character.quotes += [quote]
                character.save()
            else:
                Character(name=quote.character, quotes=[quote]).save()

        return {'quote': json.loads(quote.to_json())}, 201


class QuoteAPI(Resource):
    def get(self, id):
        return {'quote': json.loads(Quote.objects.get_or_404(id=id).to_json())}

    def put(self, id):
        if not request.json:
            abort(400)
        if 'id' in request.json or 'uri' in request.json:
            abort(403, message='Modification of the uri or id field is forbidden')

        quote = Quote.objects.get_or_404(id=id)

        for key, value in request.json.items():
            if value == '':
                try:
                    delattr(quote, key.lower())
                except AttributeError:
                    pass  # Doesn't matter that it doesn't exist.
            else:
                setattr(quote, key.lower(), value)
        quote.save()

        return {'quote': json.loads(quote.to_json())}

    def delete(self, id):
        Quote.objects.get_or_404(id=id).delete()
        return '', 204


class CharacterListAPI(Resource):
    def get(self):
        return {'characters': json.loads(Character.objects.to_json())}

    def post(self):
        if not request.json or 'name' not in request.json or 'id' in request.json or 'uri' in request.json or 'quotes' in request.json:
            abort(403, message='Does the name field exist?')

        try:
            character = Character(**request.json, quotes=3).save()
        except NotUniqueError:
            abort(
                403, message=f'The character "{request.json["character"]}" already exists.')
        except ValidationError as e:
            abort(403, message=e)

        character.uri = url_for('character', id=character.id, _external=True)
        character.save()

        return {'character': json.loads(character.to_json())}, 201


class CharacterAPI(Resource):
    def get(self, id):
        return {'character': json.loads(Character.objects.get_or_404(id=id).to_json())}

    def put(self, id):
        if not request.json:
            abort(400)
        if 'id' in request.json or 'uri' in request.json or 'quotes' in request.json:
            abort(403, message='Modification of the uri, quotes or id field is forbidden')

        character = Character.objects.get_or_404(id=id)

        for key, value in request.json.items():
            if value == '':
                try:
                    delattr(character, key.lower())
                except AttributeError:
                    pass  # Doesn't matter that it doesn't exist.
            else:
                setattr(character, key.lower(), value)
        character.save()

        return {'character': json.loads(character.to_json())}

    def delete(self, id):
        Character.objects.get_or_404(id=id).delete()
        return '', 204
