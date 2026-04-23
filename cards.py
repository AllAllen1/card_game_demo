class Card:
    def __init__(self, name, cost, card_type, description):
        self.name = name
        self.cost = cost
        self.card_type = card_type  # 'Attack', 'Defense', 'Skill'
        self.description = description

    def play(self, player, enemy):
        """Базовый метод розыгрыша карты"""
        pass

class Strike(Card):
    def __init__(self):
        super().__init__("Удар", 1, "Attack", "Наносит 8 урона.")
        self.damage = 8

    def play(self, player, enemy):
        player.current_energy -= self.cost
        enemy.current_hp -= self.damage

class Defend(Card):
    def __init__(self):
        super().__init__("Защита", 1, "Defense", "Дает 6 брони.")
        self.block = 6

    def play(self, player, enemy):
        player.current_energy -= self.cost
        player.armor += self.block