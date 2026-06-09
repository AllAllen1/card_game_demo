import json
import os
from cards import AttackCard, DefenseCard
from enemy import Goblin, Skeleton
from player import Player
from game import Game

SAVE_FILE = "save.json"

CARD_CLASSES = {
    "AttackCard": AttackCard,
    "DefenseCard": DefenseCard,
}

ENEMY_CLASSES = {
    "Goblin": Goblin,
    "Skeleton": Skeleton,
}


def save_game(game, current_state):
    data = {
        "current_state": current_state,
        "player": {
            "max_hp": game.player.max_hp,
            "current_hp": game.player.current_hp,
            "max_energy": game.player.max_energy,
            "current_energy": game.player.current_energy,
            "armor": game.player.armor,
            "hand": [type(c).__name__ for c in game.player.hand],
            "deck": [type(c).__name__ for c in game.player.deck],
            "discard_pile": [type(c).__name__ for c in game.player.discard_pile],
        },
        "enemies": [
            {
                "type": type(e).__name__,
                "current_hp": e.current_hp,
            }
            for e in game.enemies
        ],
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    game = Game.__new__(Game)
    game.current_room = None

    p_data = data["player"]
    player = Player.__new__(Player)
    player.max_hp = p_data["max_hp"]
    player.current_hp = p_data["current_hp"]
    player.max_energy = p_data["max_energy"]
    player.current_energy = p_data["current_energy"]
    player.armor = p_data["armor"]
    player.hand = [CARD_CLASSES[n]() for n in p_data["hand"] if n in CARD_CLASSES]
    player.deck = [CARD_CLASSES[n]() for n in p_data["deck"] if n in CARD_CLASSES]
    player.discard_pile = [CARD_CLASSES[n]() for n in p_data["discard_pile"] if n in CARD_CLASSES]
    game.player = player

    game.enemies = []
    for e_data in data["enemies"]:
        cls = ENEMY_CLASSES.get(e_data["type"])
        if cls:
            enemy = cls()
            enemy.current_hp = e_data["current_hp"]
            game.enemies.append(enemy)

    return game, data["current_state"]


def has_save():
    return os.path.exists(SAVE_FILE)
