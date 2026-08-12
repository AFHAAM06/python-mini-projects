import json

class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def isalive(self):
        if self.hp > 0:
            return True
        else: 
            return False

    def damage(self, target):
        target.hp -= self.attack
        print(f"{self.name} attacked {target.name} and reduced {self.attack}hp")

    def to_dict(self):
        return {"name": self.name, "hp": self.hp, "attack": self.attack}

class Enemy(Character):
    pass

weapon_damage = {"spear": 16, "sword": 20, "Bow": 18,"Large sword": 30}

rooms = {"Entrance Hall": 
            {"description": "A room full of statues holding spears",
            "exits": {
                "north": "Staircase",
                "west": "Living Room",
                "east": "Dining Room"
            },
            "enemy": Enemy("soldier", 100, 15),
            "item": "spear"
            },
        "Dining Room":
            {"description": "A long table with many chairs",
                    "exits": {
                        "north": "Lounge",
                        "west": "Entrance Hall"
                    },
                    "enemy": None,
                    "item": "Sheild"
            },
        "Lounge": 
            {"description": "A lounge room",
            "exits": {
                "north": "Kitchen",
                "south": "Dining Room",
                "west": "Entrance Hall",
            },
            "enemy": Enemy("Head Soldier", 120, 20),
            "item": "sword"
            },
        "Kitchen": 
            {"description": "A kitchen counter with meat lying there",
            "exits": {
                "south": "Lounge",
                "west": "Bedroom1",
            },
            "enemy": Enemy("Head Soldier", 120, 20),
            "item": None
            },
        "Bedroom1": 
            {"description": "A large bedroom of dark theme",
            "exits": {
                "south": "Living Room",
                "east": "Kitchen",
            },
            "enemy": Enemy("Warrior", 200, 25),
            "item": "Armor"
            },
        "Living Room": 
            {"description": "A dark room with torn curtains",
            "exits": {
                "north": "Bedroom1",
                "east": "Entrance Hall",
            },
            "enemy": Enemy("Archer", 120, 20),
            "item": "Bow"
            },
        "Staircase": 
            {"description": "A staircase leading to the final Boss dungeon",
            "exits": {
                "north": "Dungeon",
                "south": "Entrance Hall"
            },
            "enemy": None,
            "item": "Large sword"
            },
        "Dungeon": 
            {"description": "A large room with a terrifying figure",
            "exits": {
                "south": "Staircase"
            },
            "enemy": Enemy("Final Boss", 250, 30),
            "item": None
            }
            }

class Player(Character):
    def __init__(self, name, hp, attack):
        super().__init__(name, hp, attack)
        self.inventory = []
        self.current_room = "Entrance Hall"

    def damage(self, target):
        best_weapon = max(self.inventory, key=lambda item: weapon_damage.get(item, 0)) if self.inventory != [] else "no weapon"
        current_attack = weapon_damage.get(best_weapon, 5)
        target.hp -= current_attack

    def to_dict(self):
        return {"name": self.name, "hp": self.hp, "attack": self.attack, "inventory": self.inventory,"current_room":self.current_room}

def move(player):
    direction = input("Enter the direction you want to move to: ")
    if direction in rooms[player.current_room]["exits"]:
        player.current_room = rooms[player.current_room]["exits"][direction]
    else:
        print("you can't go that way")

def show_room(player):
    print(f"Current location: \n")
    print(f"{player.name} at {player.current_room} \n")
    print(f'{rooms[player.current_room]["description"]} with exits: {", ".join(rooms[player.current_room]["exits"].keys())}')

def take(player):
    if rooms[player.current_room]["item"] is not None:
        player.inventory.append(rooms[player.current_room]["item"])
        print(f'you picked up a {rooms[player.current_room]["item"]}')
        rooms[player.current_room]["item"] = None
    else:
        print(f'No item was found in the {player.current_room}')

def view_inventory(player):
    if len(player.inventory) != 0:
        print("you have the following items: \n")
        for item in player.inventory:
            print(item)
    else:
        print("your inventory is empty")

def combat(player):
    enemy = rooms[player.current_room]["enemy"]
    if enemy is not None:
        if enemy.isalive():
            while(player.isalive() and enemy.isalive()):
                player.damage(enemy)
                if enemy.isalive():
                    enemy.damage(player)
            if player.isalive():
                print("YOU WIN")
                player.hp += 25
                rooms[player.current_room]["enemy"] = None
            else:
                print("YOU LOST")
                rooms[player.current_room]["enemy"] = None
        else:
            print("you defeated the enmey")
    else:
        print("room clear")

def save_game(player):
    rooms_for_saving = {}
    for room_name, room_data in rooms.items():
        enemy = room_data["enemy"]
        if enemy is not None:
            enemy_data = enemy.to_dict()
        else:
            enemy_data = None
        rooms_for_saving[room_name] = {
            "description": room_data["description"],
            "exits": room_data["exits"],
            "enemy": enemy_data,
            "item": room_data["item"]
        }
    save_data = {"player_info": player.to_dict(), "room":rooms_for_saving}
    with open("saved_game.json","w") as f:
        json.dump(save_data,f)

def load_game():
    try:
        global rooms
        with open("saved_game.json","r") as f:
            data = json.load(f)
            player = Player(name = data["player_info"]["name"], hp = data["player_info"]["hp"], attack = data["player_info"]["attack"])
            player.inventory = data["player_info"]["inventory"]
            player.current_room = data["player_info"]["current_room"]
            rooms_loaded = {}
            for room_name, room_data in data["room"].items():
                enemy_dict = room_data["enemy"]
                if enemy_dict is not None:
                    enemy = Enemy(name=enemy_dict["name"], hp=enemy_dict["hp"], attack=enemy_dict["attack"])
                else:
                    enemy = None
                rooms_loaded[room_name] = {
                    "description": room_data["description"],
                    "exits": room_data["exits"],
                    "enemy": enemy,
                    "item": room_data["item"]
                }
            rooms = rooms_loaded
            return player
    except FileNotFoundError:
        return None

def main():
    player = load_game()
    if player is not None:
        playing = True

    else:
        print("No saved files yet")
        print("new game starting")
        player = Player(input("Enter a name"),200,5)
        playing = True

    while(player.isalive() and playing):
        show_room(player)
        print("enter 'q' to quit\nenter 'move' to move\nenter 'take' to take \nenter 'shoe inventory' to view inventory\nenter 'attack' to start combat\nenter 'save' to save the game")
        command = input("> ").lower()
        if command == "q":
            playing = False

        elif command == "move":
            move(player)

        elif command == "take":
            take(player)

        elif command == "show inventory":
            view_inventory(player)

        elif command == "attack":
            combat(player)

        elif command == "save":
            save_game(player)

        else:
            print("invalid input")

if __name__ == "__main__": main()