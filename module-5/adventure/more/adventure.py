from room import Room
from item import Item
import re


class Adventure():

    # Create rooms and items for the appropriate 'game' version.
    def __init__(self, game):
        
        self.game_data_file= f"data/{game}Adv.dat"
        self.reset()


    # Load rooms from filename in two-step process
    def load_rooms(self, filename):
        # Store filename, so we can reset later
        self.filename = filename
        with open(filename) as f:
            # Start reading file, first section contains room definitions:
            line = f.readline()
            while line:
                self._load_rooms_from_line(line)
                line = f.readline()
                if line =="\n": break
            
            # Continue reading file, next section contains directions:
            while line:
                line = f.readline()
                if line =="\n": break
                self._load_directions_from_line(line)
                    
            # Continue reading file, next section contains items:
            while line:
                line = f.readline()
                if line =="\n" or line == "": break
                self._load_items_from_line(line);
                

    # Helper functions for line parsing:
    def _load_rooms_from_line(self, line):
        # unpack list into vars
        identifier, name, description = line.split("\t");
        self.rooms[int(identifier)] = Room(int(identifier), name, description)
        

    def _load_directions_from_line(self, line):
        data = line.strip().split("\t");
        # first "field" of this line conatins the ID to the source room, 
        # pop it from the list and get the room from the internal rooms dictionary
        source_room = self.rooms[int(data.pop(0))]
        
        #convert list to Iterator:
        data = iter(data) 
        for direction in data:
            # By calling next() on list iterator, the list pointer moves to the next value:
            destination_room_identifier = next(data)
            match = re.search(r"^(?P<id>\d+)\/(?P<item_name>[A-Z]+)$", destination_room_identifier)
            if match:
                destination_room_identifier = int(match.group('id'))
                item_name = match.group('item_name')
                destination_room = self.rooms[destination_room_identifier]
                source_room.add_connection_with_item_name(direction, destination_room, item_name)
            else:
                destination_room_identifier = int(destination_room_identifier)
                destination_room = self.rooms[destination_room_identifier]
                source_room.add_connection(direction, destination_room)
        
    def _load_items_from_line(self, line):
        name, desc, r = line.strip().split("\t")
        r = int(r)
        assert r in self.rooms
        self.rooms[r].add_item(Item(name, desc))
    # END
    
    def reset(self):
        # Rooms is a dictionary that maps a room number to the corresponding room object
        self.rooms = {}

        # Inventory is a dictionary that holds items picked up during game
        self.inventory = {}

        # Load room structures
        self.load_rooms(self.game_data_file)
        
        self.load_synonyms()
        
        # Game always starts in room number 1, so we'll set it after loading
        assert 1 in self.rooms
        self.current_room = self.rooms[1]

    # Avoid direct contact with object properties:
    def room(self):
        return self.current_room;
        
    def get_long_description(self):
        return self.room().get_long_description()

    # Pass along the long/short (depending on visit history) description of the current room
    def get_description(self):
        return str(self.room())
    
    # Returns False or the room on which to force to go back to
    def is_forced(self):
        room_or_false = False
        for item_name in self.get_inventory():
            if self.room().has_connection_with_item_name("FORCED", item_name):
                room_or_false = self.room().get_connection_with_item_name("FORCED", item_name);
                break
        
        if False == room_or_false and self.current_room.has_connection("FORCED"):
            room_or_false = self.current_room.get_connection("FORCED")
            
        return room_or_false
        
    # Look up the command in the list of synonyms and return it if found or return the original cmd
    def get_command(self, cmd):
        cmd = cmd.upper()
        # This might be a synonym, let's check it and freturn the corresponding cmd:
        return self.synonyms[cmd] if cmd in self.synonyms else cmd
        
    def move_to_room(self, room):
        assert type(room).__name__ == 'Room' or type(room).__name__ == 'int'
        # Before leaving this room, mark it as visited
        self.room().set_visited()
        
        if (type(room).__name__ == 'int'):
            assert room in self.rooms
            self.current_room = self.rooms[room]
        else:
            assert room.identifier in self.rooms
            self.current_room = room
        
    def take_item(self, item_name):
        assert self.room().has_item(item_name)
        item = self.room().take_item(item_name)
        item.pickup()
        self.inventory[item_name] = item
        return item
        
    def drop_item(self, item_name):
        assert item_name in self.inventory
        item = self.inventory[item_name]
        item.drop()
        self.inventory.pop(item_name)
        self.room().add_item(item)
        return item
        
    def in_inventory(self, item_name):
        return item_name in self.inventory
        
    def get_inventory(self):
        return self.inventory
        
    def get_inventory_item(self, item_name):
        assert item_name in self.inventory
        return self.inventory[item_name]
        
    def reset_inventory(self):
        self.inventory = {}
        
    # Move to a different room by changing "current" room, if possible
    def move(self, direction):
        # since our data file uses uppercase only for directions, make sure we move to that as well;
        direction = direction.upper()
        
        if not self.current_room.has_connection(direction): 
            return False
            
        moved = False
        for item_name in self.get_inventory():
            if self.room().has_connection_with_item_name(direction, item_name):
                room = self.room().get_connection_with_item_name(direction, item_name);
                self.move_to_room(room)
                moved = True
                break
            
        if not moved:
            room = self.room().get_connection(direction)
            self.move_to_room(room)
        
    #Load synonyms from file:
    def load_synonyms(self):
        self.synonyms = {}
        lines = open("data/Synonyms.dat", 'r')
        for line in lines:
            # unpack list into vars
            synonym, direction = line.strip().split("=")
            self.synonyms[synonym.upper()] = direction
        

def proc(command):
    command = command.lower();
    # Not part of the assignment, cheat to go directly to a specific room
    match = re.findall(r"^move\s+(\d+)$", command)
    if match:
        command = "move"
        moveTo = int(match[0])
    # END

    match = re.search(r"^(?P<command>take|drop) (?P<item_name>[a-z]+)$", command)
    if match:
        command = match.group('command')
        item_name = match.group('item_name').upper()

    # Escape route
    if command == "help":
        print("You can move by typing directions such as EAST/WEST/IN/OUT")
        print("QUIT quits the game.")
        print("HELP prints instructions for the game.")
        print("LOOK lists the complete description of the room and its contents.")

        # Not part of assignment
        print("CHEAT prints all possible moves.")
        print("MOVE <n> move directluy to room <n> (if room exists).")
        # END
    elif command == "reset":
        adventure.reset()
        print(adventure.get_description())
    elif command == "take":
        if False == adventure.room().has_item(item_name):
            print("No such item")
            # print("There is no item {} in this room.".format(item_name))
        elif True == adventure.in_inventory(item_name):
            print("No such item")
            # print("You already have {} in your inventory.".format(item_name))
        else:
            adventure.take_item(item_name)
            print("{} taken".format(item_name))
    elif command == "drop":
        if item_name == 'ALL':
            inventory = adventure.reset_inventory()
        elif not item_name in adventure.get_inventory():
            print("No such item: you do not have {} in your inventory.".format(item_name))
        else:
            adventure.drop_item(item_name)
            print("{} dropped".format(item_name))
    elif command == "cheat":
        # Not part of assignment
        print("You are now in room #{}, possible moves: ".format(adventure.room().identifier), end='')
        for direction in adventure.room().connections:
            print("{}=>#{} ".format(direction, adventure.room().connections[direction].identifier), end=' ')
        print("")
        # END 
    elif command == "win":
        win = ["MOVE 1", "IN", "TAKE KEYS", "OUT", "DOWN", "DOWN",
                 "DOWN", "DOWN", "TAKE LAMP", "IN", "WEST",
                 "WEST", "WEST", "TAKE BIRD", "WEST", "DOWN",
                 "SOUTH", "TAKE NUGGET", "OUT", "DROP NUGGET", "UP",
                 "EAST", "EAST", "EAST", "TAKE ROD", "WEST",
                 "WEST", "WEST", "DOWN", "TAKE NUGGET", "WEST",
                 "WAVE", "TAKE DIAMOND", "WEST", "SOUTH", "SOUTH",
                 "EAST", "NORTH", "NORTH", "TAKE CHEST", "OUT",
                 "WEST", "DOWN", "WEST", "DOWN", "NORTH",
                 "EAST", "TAKE COINS", "OUT", "NORTH", "DOWN",
                 "EAST", "DROP LAMP", "DROP BIRD", "DROP NUGGET", "DROP COINS",
                 "NORTH", "TAKE EMERALD", "OUT", "TAKE LAMP", "TAKE BIRD",
                 "TAKE NUGGET", "TAKE COINS", "WEST", "WEST", "WEST",
                 "DOWN", "WATER", "TAKE EGGS", "NORTH", "DOWN",
                 "OUT", "EAST", "EAST", "EAST", "UP",
                 "SOUTH", "SOUTH", "WEST", "WAVE", "WEST",
                 "SOUTH", "NORTH", "NORTH", "EAST", "DOWN",
                 "EAST", "EAST", "XYZZY", "NORTH"]
        adventure.reset();
        for cmd in win:
            proc(cmd)
    elif command == "move":
        #  Not part of the assignment, cheat to go directly to a specific room
        if moveTo in adventure.rooms:
            adventure.move_to_room(moveTo)
            print(adventure.get_description())
        else:
            print("Cannot move to a non-exisiting room")
        # END
    elif command == "look":
        print(adventure.get_long_description())
    elif command == "inventory":
        inventory = adventure.get_inventory()
        if not inventory:
            print("Your inventory is empty")
        for item_name in inventory:
            item = adventure.get_inventory_item(item_name)
            print(str(item))
    else:
        if False == adventure.move(command):
            print("Invalid command")
        else:
            while True:
                forced_room = adventure.is_forced()
                print(adventure.get_description())
                if False == forced_room:
                    break
                else:
                    adventure.move_to_room(forced_room)


if __name__ == "__main__":
    from sys import argv

    # Check command line arguments
    if len(argv) not in [1,2]:
        print("Usage: python adventure.py [name]")
        exit(1)

    # Load the requested game or else Crowther
    if len(argv) == 1:
        game_name = "Crowther"
    elif len(argv) == 2:
        game_name = argv[1]

    # Create game
    adventure = Adventure(game_name)
    
    # Welcome user
    print("Welcome to Adventure.\n")

    # Print very first room description
    print(adventure.get_description())
    
    # Prompt the user for commands until they type QUIT
    while True:

        # Prompt
        command = adventure.get_command(input("> ")).lower()
        if command == "quit":
            break
        proc(command)
        

