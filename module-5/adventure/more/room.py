class Room():
     def __init__(self, identifier: int, name: str, description: str):
         self.identifier = identifier
         # Clean up String values (such as newlines ...):
         self.name = name.strip()
         self.description = description.strip()
         self.connections = {}
         self.connections_with_items = {}
         self.items = {}
         self.visited = False
         
     def add_connection(self, direction: str, room):
         #Accept only Room objects:
         assert type(self).__name__ == type(room).__name__
         self.connections[direction] = room
         
     def add_connection_with_item_name(self, direction: str, room, item_name: str):
         assert type(self).__name__ == type(room).__name__
         identifier = direction+'/'+item_name
         self.connections_with_items[identifier] = room
         
     def has_connection(self, direction):
         return direction in self.connections
         
     def has_connection_with_item_name(self, direction: str, item_name: str):
         identifier = direction+'/'+item_name
         return identifier in self.connections_with_items
         
     def get_connection(self, direction: str):
         assert True == self.has_connection(direction)
         return self.connections[direction]
         
     def get_connection_with_item_name(self, direction: str, item_name: str):
         assert True == self.has_connection_with_item_name(direction, item_name)
         identifier = direction+'/'+item_name
         return self.connections_with_items[identifier]
         
     def set_visited(self):
         self.visited = True
         
     def already_visited(self):
         return self.visited == True

     def add_item(self, item):
         #Accept only Room objects:
         assert type(item).__name__ == 'Item'
         self.items[item.name] = item
     
     def has_items(self):
        return len(self.items) > 0
    
     def get_items(self):
        return self.items
    
     def has_item(self, name):
        return name in self.items
    
     def take_item(self, name):
        assert self.has_item(name)
        item = self.items[name]
        self.items.pop(name)
        return item
        
     def get_item(self, name):
        assert self.has_item(name)
        return self.items[name]
        
     def get_short_description(self):
        # return "[{}] {}".format(self.identifier, self.name)
        return self.name
        
     def get_long_description(self):
         desc = "[{}] {}".format(self.identifier, self.description)
         desc = self.description
         if self.has_items():
             for name in self.get_items():
                 item = self.get_item(name)
                 if not item.picked_up:
                     desc += "\n" + str(item)
         return desc
         
        
     # Magic method called when casting this object str, eg str(item)
     def __str__(self):
        return self.get_short_description() if self.already_visited() else self.get_long_description()
        