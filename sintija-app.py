#created a simple webb application
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return {'Hello': 'it is nice to see you here again!'}
    
api.add_resource(Greeting, '/')

if __name__ == '__main__':
    app.run(debug=True)
    

