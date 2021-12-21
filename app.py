from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings

app = Flask(__name__)

# Define method to manage exceptions
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

# Assign handle_error method to all exceptions
for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

api = Api(app)
api.prefix = '/api'

# Import contollers
from endpoints.tfidf.resource import TfidfResource
from endpoints.idf.resource import IdfGenratorResource

# Define routes and handlers 
api.add_resource(TfidfResource, '/tfidf', '/tfidf')
api.add_resource(IdfGenratorResource, '/idfGenerator', '/idfGenerator')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)