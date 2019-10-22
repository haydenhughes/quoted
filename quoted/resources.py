import json
from flask import request
from flask_restful import Resource, abort
from mongoengine import ValidationError, NotUniqueError


class QueryAPI(Resource):
    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.query = kwargs['query']

    def get(self):
        return {self.endpoint: json.loads(self.query.objects.to_json())}

    def post(self):
        if not request.json:
            abort(400)

        try:
            document = self.query(**request.json).save()
        except NotUniqueError:
            abort(
                403, message=f'Already exists.')
        except ValidationError as e:
            abort(400, message=e)

        document.uri = url_for(
            document.__class__.__name__.lower(), id=document.id, _external=True)
        document.save()

        return {self.endpoint: json.loads(document.to_json())}, 201


class DocumentAPI(Resource):
    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.query = kwargs['query']

    def get(self, id):
        return {self.endpoint: json.loads(self.query.objects.get_or_404(id=id).to_json())}

    def put(self, id):
        if not request.json:
            abort(400)

        document = self.query.objects.get_or_404(id=id)

        for key, value in request.json.items():
            if value == '':
                try:
                    delattr(document, key.lower())
                except AttributeError:
                    pass  # Doesn't matter that it doesn't exist.
            else:
                setattr(document, key.lower(), value)
        document.save()

        return {self.endpoint: json.loads(document.to_json())}

    def delete(self, id):
        self.query.objects.get_or_404(id=id).delete()
        return '', 204
