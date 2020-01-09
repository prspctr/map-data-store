from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", password="mighty_youthful_tomahawk")

graph.schema.create_uniqueness_constraint('Room', 'id')

# graph.delete_all()

room_count = 0


def add_room(exit_data, **room_data):
    room_1 = Node("Room", **room_data)
    graph.merge(room_1, "Room", "id")
    global room_count
    room_count += 1
    room_id = room_data.get("id", None)
    print(f"Added Room {room_id} | {room_count} rooms total")
