from room import Room

class Adventure():

    # Create rooms and items for the appropriate 'game' version.
    def __init__(self, game):

        # Rooms is a dictionary that maps a room number to the corresponding room object
        self.rooms = {}

        # Load room structures
        self.load_rooms(f"data/{game}Adv.dat")
        
        self.load_synonyms()
        
        # Game always starts in room number 1, so we'll set it after loading
        assert 1 in self.rooms
        self.current_room = self.rooms[1]

    # Load rooms from filename in two-step process
    def load_rooms(self, filename):
        with open(filename) as f:
            # Start reading file, first section contains room definitions:
            line = f.readline()
            while line:
                # unpack list into vars
                identifier, name, description = line.split("\t");
                self.rooms[int(identifier)] = Room(int(identifier), name, description)
                line = f.readline()
                if (line =="\n"): break
            
            # Continue reading file, next section contains directions:
            while line:
                line = f.readline()
                if (line =="\n"): break
                data = line.strip().split("\t");
                # first "field" of this line conatins the ID to the source room, 
                # pop it from the list and get the room from the internal rooms dictionary
                source_room = self.rooms[int(data.pop(0))]
                
                #convert list to Iterator:
                data = iter(data) 
                for direction in data:
                    # By calling next() on list iterator, the list pointer moves to the next value:
                    destination_room_identifier = int(next(data))
                    destination_room = self.rooms[destination_room_identifier]
                    source_room.add_connection(direction, destination_room)
                    
    def get_long_description(self):
        return self.current_room.description

    # Pass along the long/short (depending on visit history) description of the current room
    def get_description(self):
        return self.current_room.name if self.current_room.already_visited() else self.get_long_description()
    
    # Returns False or the room on which to force to go back to
    def is_forced(self):
        return self.current_room.get_connection("FORCED") if self.current_room.has_connection("FORCED") else False
        
    # Look up the command in the list of synonyms and return it if found or return the original cmd
    def get_command(self, cmd):
        cmd = cmd.upper()
        # This might be a synonym, let's check it and freturn the corresponding cmd:
        return self.synonyms[cmd] if cmd in self.synonyms else cmd
        
    # Move to a different room by changing "current" room, if possible
    def move(self, direction):
        # since our data file uses uppercase only for directions, make sure we move to that as well;
        direction = direction.upper()
        
        if not self.current_room.has_connection(direction): 
            return False
            
        # Before leaving this room, mark it as visited
        self.current_room.set_visited()
        self.current_room = self.current_room.get_connection(direction)
        
    #Load synonyms from file:
    def load_synonyms(self):
        self.synonyms = {}
        lines = open("data/Synonyms.dat", 'r')
        for line in lines:
            # unpack list into vars
            synonym, direction = line.strip().split("=")
            self.synonyms[synonym.upper()] = direction
        

if __name__ == "__main__":
    
    from sys import argv

    # Check command line arguments
    if len(argv) not in [1,2]:
        print("Usage: python adventure.py [name]")
        exit(1)

    # Load the requested game or else Tiny
    if len(argv) == 1:
        game_name = "Tiny"
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

        # Escape route
        if command == "quit":
            break
        elif command == "help":
            print("You can move by typing directions such as EAST/WEST/IN/OUT")
            print("QUIT quits the game.")
            print("HELP prints instructions for the game.")
            print("CHEAT prints all possible moves.")
            print("LOOK lists the complete description of the room and its contents.")
        elif command == "cheat":
            print("Possible moves: ", end='')
            for direction in adventure.current_room.connections:
                print(direction, end=' ')
            print("")
        elif command == "look":
            print(adventure.get_long_description())
        else:
            if False == adventure.move(command):
                print("Invalid command")
            else:
                forced_room = adventure.is_forced()
                if False == forced_room:
                    print(adventure.get_description())
                else:
                    print(adventure.get_long_description())
                    adventure.current_room = forced_room
                    print(adventure.get_description())

