from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from app import add_room, add_connection


app = Flask(__name__)
api = Api(app)


class Room(Resource):
    body_parser = reqparse.RequestParser()
    body_parser.add_argument("id", type=int, required=True,
                             help="Missing Id of the room")
    body_parser.add_argument("title", type=str, required=False,
                             help="Title of the room needs to be a string")
    body_parser.add_argument("description", type=str, required=False,
                             help="Description of the room needs to be a string")
    body_parser.add_argument("x", type=int, required=True,
                             help="Missing X Coordinate for the room")
    body_parser.add_argument("y", type=int, required=True,
                             help="Missing Y Coordinate for the room")

    exits_parser = reqparse.RequestParser()
    exits_parser.add_argument("n", type=int, required=False,
                              help="Room Id for room to the North needs to be an integer")
    exits_parser.add_argument("e", type=int, required=False,
                              help="Room Id for room to the East needs to be an integer")
    exits_parser.add_argument("s", type=int, required=False,
                              help="Room Id for room to the South needs to be an integer")
    exits_parser.add_argument("w", type=int, required=False,
                              help="Room Id for room to the West needs to be an integer")

    def post(self):
        body = Room.body_parser.parse_args()
        exits = Room.exits_parser.parse_args(req=Room.body_parser)
        add_room(**body)
        return {"msg": f"""Room {body.get("id", None)} successfully added!"""}


class RoomConnection(Resource):
    body_parser = reqparse.RequestParser()
    body_parser.add_argument("originId", type=int, required=True,
                             help="Missing Id for origin Room")
    body_parser.add_argument("destinationId", type=int, required=True,
                             help="Missing Id for destination Room")
    body_parser.add_argument("direction", type=str, required=True,
                             help="Missing direction for the connection")

    def post(self):
        body = RoomConnection.body_parser.parse_args()

        room_1_id = body.get("originId", None)
        room_2_id = body.get("destinationId", None)
        direction = body.get("direction", None)

        add_connection(room_1_id, room_2_id, direction)

        return {"msg": f"""Room {room_1_id} successfully connected ({direction}) to Room {room_2_id}!"""}


api.add_resource(Room, "/rooms")
api.add_resource(RoomConnection, "/connections")

# app.run(port=5000, debug=True)
app.run(port=5000)
