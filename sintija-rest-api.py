#converting app into RESTful service

from flask import Flask, request 
from flask_restful import reqparse, abort, Resource, Api
from subprocess import Popen, PIPE

app = Flask(__name__)
api = Api(app)

# creating my database of ice cream flavours
SELECTION = {'icecream1': {'description': 'Chocolate ice cream with fudge brownies and milk chocolate ganache'},
             'icecream2': {'description': 'Raspberry ice cream with raspberry sauce and white chocolate chips'}
            }
    
class SelectionList(Resource):
             
    def get(self):
        print("debug: sending full list") 
        return SELECTION
    
    def post(self):
        args = parser.parse_args()
        icecream_id = int(max(SELECTION.keys()).lstrip('icecream')) + 1
        icecream_id = 'icecream%i' % icecream_id
        SELECTION[icecream_id] = {'description': args['description']}
        print("debug: added description with id '{}'".format(icecream_id))
        return SELECTION[icecream_id], 201

class Selection(Resource):
    def get(self, icecream_id):
        abort_if_icecream_is_not_available(icecream_id)
        return SELECTION[icecream_id]
        
    def put(self, icecream_id):
        args = parser.parse_args()
        description = {'description': args['description']}
        SELECTION[icecream_id] = description
        return description, 201
    
    def delete(self, icecream_id):
        print("debug: deleting task with id '{}'".format(icecream_id))
        abort_if_icecream_is_not_available(icecream_id)
        del SELECTION[icecream_id]
        return {'message': 'Description "{}" deleted'.format(icecream_id)}, 204

class Ping(Resource):
    def get(self):
        process = Popen(["ping 8.8.8.8 -c 2"],
                shell=True, stdout=PIPE, stderr=PIPE)
        rc = process.wait()
        return process

def abort_if_icecream_is_not_available(icecream_id):
    if icecream_id not in SELECTION:
        abort(
            404,
            message='Icecream to select by id: {} is not available!'.format(icecream_id)
        )
             
parser = reqparse.RequestParser()
parser.add_argument('description')
    
api.add_resource(SelectionList, '/selection')
api.add_resource(Selection, '/selection/<icecream_id>')
api.add_resource(Ping, '/ping')


if __name__ == '__main__': 
    app.run(debug=True)
