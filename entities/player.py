import random
from cards import Strike, Defend

class Player:
    def __init__(self):
        self.max_hp = 50
        self.current_hp = 50
        self.max_energy = 3
        self.current_energy = 3
        self.armor = 0
        
        # Инициализация колоды: 5 ударов и 5 защит
        self.deck = [Strike() for _ in range(5)] + [Defend() for _ in range(5)]
        self.draw_pile = self.deck.copy()
        random.shuffle(self.draw_pile) # Перемешиваем стопку
        
        self.discard_pile = []
        self.hand = []

    def draw_cards(self, count):
        for _ in range(count):
            if not self.draw_pile:
                if not self.discard_pile:
                    break  # Нет карт ни в колоде, ни в сбросе
                # Замешиваем сброс в колоду
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile.clear()
                random.shuffle(self.draw_pile)
            
            self.hand.append(self.draw_pile.pop())

    def discard_hand(self):
        self.discard_pile.extend(self.hand)
        self.hand.clear()

    def start_turn(self):
        self.current_energy = self.max_energy
        self.armor = 0  # Броня сгорает в начале нового хода (после атак врагов)
        self.draw_cards(5)