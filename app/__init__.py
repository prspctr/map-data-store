from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", password="mighty_youthful_tomahawk")

graph.schema.create_uniqueness_constraint('Room', 'id')

# graph.delete_all()

room_count = 0
connection_count = 0


def add_room(**room_data):
    room = Node("Room", **room_data)
    graph.merge(room, "Room", "id")

    global room_count
    room_count += 1
    room_id = room_data.get("id", None)
    print(f"Added Room {room_id} | {room_count} rooms total")


def add_connection(room_1_id, room_2_id, direction):
    room_1 = graph.nodes.match("Room", id=room_1_id).first()
    room_2 = graph.nodes.match("Room", id=room_2_id).first()

    if not room_1:
        room_1 = Node("Room", id=room_1_id)

    if not room_2:
        room_2 = Node("Room", id=room_2_id)

    rel = Relationship(room_1, "CONNECTS_TO", room_2, direction=direction)

    graph.merge(rel, "Room", "id")

    global connection_count
    connection_count += 1
    print(f"Room {room_1_id} -> {direction} -> Room {room_2_id}")
