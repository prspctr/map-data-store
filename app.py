from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Room(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(Room, "/rooms")

app.run(port=5000, debug=True)