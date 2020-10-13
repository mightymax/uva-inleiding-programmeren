class Room():
     def __init__(self, identifier: int, name: str, description: str):
         self.identifier = identifier
         # Clean up String values (such as newlines ...):
         self.name = name.strip()
         self.description = description.strip()
         self.connections = {}
         self.visited = False
         
     def test(self):
         print(type(self).__name__)
     
     def add_connection(self, direction: str, room):
         #Accept only Room objects:
         assert type(self).__name__ == type(room).__name__
         self.connections[direction] = room
         
     def has_connection(self, direction):
         return direction in self.connections
         
     def get_connection(self, direction):
         assert True == self.has_connection(direction)
         return self.connections[direction]
         
     def set_visited(self):
         self.visited = True
         
     def already_visited(self):
         return self.visited == True
