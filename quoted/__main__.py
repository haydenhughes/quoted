from flask import Flask
from flask_restful import Api
from mongoengine import connect
from .api import QuoteAPI, QuoteListAPI

app = Flask(__name__)
app.config.from_pyfile('../quoted.cfg')
api = Api(app)
connect('quoted', host=app.config['MONGODB_HOST'])

api.add_resource(QuoteListAPI, '/api/v1.0/quotes', endpoint='quotes')
api.add_resource(QuoteAPI, '/api/v1.0/quotes/<id>', endpoint='quote')

if __name__ == '__main__':
    app.run()
