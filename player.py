from cards import AttackCard, DefenseCard

class Player:
    def __init__(self):
        self.max_hp = 50
        self.current_hp = 50
        self.max_energy = 3
        self.current_energy = 3
        self.armor = 0
        self.hand = []
        self.deck = []
        self.discard_pile = []

    def draw_cards(self, amount):
        # Выдаем базовые карты для теста, чтобы интерфейс мог их отобразить
        if not self.hand:
            self.hand = [AttackCard(), DefenseCard(), AttackCard(), DefenseCard()]

    def discard_hand(self):
        self.discard_pile.extend(self.hand)
        self.hand.clear()

    def start_turn(self):
        self.current_energy = self.max_energy
        self.armor = 0
        self.draw_cards(5)