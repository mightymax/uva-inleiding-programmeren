class Item():
     def __init__(self, name: str, description: str):
         self.name = name
         self.description = description
         self.picked_up = False
         
     def picked_up(self):
         return self.picked_up
         
     def pickup(self):
         self.picked_up = True

     def drop(self):
         self.picked_up = False
         
     # Magic method called when casting this object str, eg str(item)
     def __str__(self):
         return "{}: {}".format(self.name, self.description)