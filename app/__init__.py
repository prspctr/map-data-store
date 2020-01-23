from py2neo import Graph, Node, Relationship, walk

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


def getRoomById(room_id):
    room = graph.nodes.match("Room", id=room_id).first()

    if not room:
        return None

    return room


def getRoomByTitle(title):
    room = graph.nodes.match("Room", title=title).first()

    if not room:
        return None

    return room


def getShortestPath(origin_id, destination_id):
    path = graph.run("""MATCH (start:Room{id: $origin_id}), (end:Room{id: $destination_id}),
    p = shortestPath((start)-[rel:CONNECTS_TO*]->(end))
    RETURN p""", parameters={"origin_id": origin_id, "destination_id": destination_id}).evaluate()

    room_ids = []
    directions = []

    for i, p in enumerate(walk(path)):
        if type(p) is Node:
            room_ids.append(p["id"])

        if type(p) is Relationship.type("CONNECTS_TO"):
            directions.append(p["direction"])

    data = []
    room_ids.pop(0)
    index = 0

    while index < len(room_ids):
        data.append({"room_id": room_ids[index],
                     "direction": directions[index]})
        index += 1

    return data


if __name__ == "__main__":
    room1 = getRoomById(47)
    room2 = getRoomById(467)
    print(getShortestPath(room1["id"], room2["id"]))
