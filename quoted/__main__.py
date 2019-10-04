import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
from .api import QuoteAPI, QuoteListAPI

app = Flask(__name__)
api = Api(app)
connect('quoted', host=os.environ.get('MONGODB_HOST',
                                      'mongodb://127.0.0.1:27017/quoted'))

api.add_resource(QuoteListAPI, '/api/v1.0/quotes', endpoint='quotes')
api.add_resource(QuoteAPI, '/api/v1.0/quotes/<id>', endpoint='quote')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
