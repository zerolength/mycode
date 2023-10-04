from datetime import date

class Room:
    def __init__(self, name, size, furniture=None, npc_entities=None, consumables=None, artifacts=None, environmental_conditions=None, adjacent_rooms=None):
        self.name = name
        self.size = size
        self.furniture = furniture or []
        self.npc_entities = npc_entities or []
        self.consumables = consumables or []
        self.artifacts = artifacts or []
        self.environmental_conditions = environmental_conditions or []
        self.adjacent_rooms = adjacent_rooms or []  # List of adjacent rooms

    def describe(self):
        print(f"You are in the {self.name}.")
        print(f"This room is {self.size} square feet in size.")
        print("Furniture in the room: ", ', '.join(self.furniture))
        print("NPC entities in the room: ", ', '.join(self.npc_entities))
        print("Consumables in the room: ", ', '.join(self.consumables))
        print("Artifacts in the room: ", ', '.join(self.artifacts))
        print("Environmental conditions: ", ', '.join(self.environmental_conditions))
        print("Adjacent rooms: ", ', '.join(room.name for room in self.adjacent_rooms))

class Player:
    def __init__(self, name, age, birthday, conditions=None, location=None):
        self.name = name
        self.age = age
        self.birthday = birthday
        self.conditions = conditions or []
        self.location = location
        self.location_history = []
    def describe(self):
        print(f"Player's name: {self.name}")
        print(f"Player's age: {self.age}")
        print(f"Player's birthday: {self.birthday.strftime('%Y-%m-%d')}")
        print("Player's conditions: ", ', '.join(self.conditions))
#        print(f"Path History",': '.join(self.location_history))
class Consumable:
    def __init__(self, name, quantity, condition_T, condition_K, condition_E, condition_C, condition_Y):
        self.name = name
        self.quantity = quantity
        self.condition_T = condition_T
        self.condition_K = condition_K
        self.condition_E = condition_E
        self.condition_C = condition_C
        self.condition_Y = condition_Y
    def quantitycheck(self):
        if self.quantity == 0:
            self.__del__()
    def __del__(self):
        print("You have used up {self.name}, what happened to Frugality")


# Create rooms with adjacency information
lobby = Room(
    name="Lobby",
    size=200,
    furniture=["sofa", "lathe", "stove"],
    environmental_conditions=["cold"],
    consumables=["firewood", "blanket"],
    adjacent_rooms=[]
)

kitchen = Room(
    name="Kitchen",
    size=150,
    furniture=["bed", "oven", "countertop", "band saw"],
    environmental_conditions=["warm"],
    consumables=["rabbit", "hammer"],
    adjacent_rooms=[]
)

meeting_room = Room(
    name="Meeting Room",
    size=100,
    npc_entities=["Picard"],
    furniture=["bathtub"],
    consumables=["bathrobe"],
    adjacent_rooms=[]
)

# Set room connections
lobby.adjacent_rooms = [kitchen, meeting_room]
kitchen.adjacent_rooms = [lobby]
meeting_room.adjacent_rooms = [lobby]

#Set consumables
firewood = Consumable(name="Firewood", quantity=100, condition_T=20, condition_K=0, condition_E=0, condition_C=0, condition_Y=0)
blanket = Consumable(name="Blanket", quantity=3, condition_T=20, condition_K=0, condition_E=0, condition_C=0, condition_Y=0)
rabbit = Consumable(name="Rabbit", quantity=2, condition_T=40, condition_K=3, condition_E=0, condition_C=0, condition_Y=0)
hammer = Consumable(name="Hammer", quantity=1, condition_T=20, condition_K=0, condition_E=0, condition_C=0, condition_Y=0)
bathrobe = Consumable(name="Bathrobe", quantity=2, condition_T=20, condition_K=1, condition_E=0, condition_C=0, condition_Y=0)

# Prompt the player for their information
player_name = input("Enter your name: ")
player_age = int(input("Enter your age: "))
player_birthday = input("Enter your birthday (YYYY-MM-DD): ")
player_birthday = date.fromisoformat(player_birthday)

# Ask for adjectives to describe conditions
print("Describe yourself using a few adjectives.")
player_conditions = input("Adjectives (comma-separated): ").split(',')

# Create the player object
player = Player(name=player_name, age=player_age, birthday=player_birthday, conditions=player_conditions)

# Initialize the player's location to the lobby
player.location = lobby
player.location_history.append(player.location)
# Main game loop
while True:
    # Describe the player and the current room
    player.describe()
    player.location.describe()

    # Player interaction menu
    print("\nWhat would you like to do?")
    print("1. Go to another room")
    print("2. Use consumables")
    print("3. Interact with artifacts and furniture")
    print("4. Quit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        # Go to another room
        print("Available rooms to go:")
        for i, room in enumerate(player.location.adjacent_rooms, start=1):
            print(f"{i}. {room.name}")

        room_choice = input("Enter the number of the room you want to go to: ")
        try:
            room_choice = int(room_choice)
            if 1 <= room_choice <= len(player.location.adjacent_rooms):
                new_room = player.location.adjacent_rooms[room_choice - 1]
                player.location = new_room
                print(f"You have entered the {new_room.name}.")
#                player.location_history.append(new_room)
            else:
                print("Invalid room choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    elif choice == "2":
        # Use consumables
        print("Available consumables:")
        for i, consumable in enumerate(player.location.consumables, start=1):
            print(f"{i}. {consumable}")

        consumable_choice = input("Enter the number of the consumable you want to use: ")
        try:
            consumable_choice = int(consumable_choice)
            if 1 <= consumable_choice <= len(player.location.consumables):
                used_consumable = player.location.consumables.pop(consumable_choice - 1)
                print(f"You have used the {used_consumable}.")
            else:
                print("Invalid consumable choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    elif choice == "3":
        # Interact with artifacts and furniture
        print("Available artifacts and furniture:")
        for i, item in enumerate(player.location.artifacts + player.location.furniture, start=1):
            print(f"{i}. {item}")

        interaction_choice = input("Enter the number for the action to take: ")
        try:
            interaction_choice=int(interaction_choice)
            if 1<= interaction_choice <= len(player.location.furniture):
                interacted_furniture = player.location.furniture.pop(interaction_choice -1)
                used_target=input("target consumable? Leave blank if none.")
                print(f"You have sudoed {interaction_choice} on {used_target}.") #need to add consumable history check
            else:
                print("not implemented due to budget constraint")
        except ValueError:
                print("try to be typefluid are you?")

    elif choice == '4':
        print("So you think you can quit? wait till the dev milk enough attention to finish his while loop")


