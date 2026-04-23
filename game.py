from entities.player import Player
from entities.enemy import Enemy

class Game:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy()
        # Выдаем стартовую руку при начале игры
        self.player.draw_cards(5)
        self.current_room = None
        # Здесь в будущем будет инициализация колоды и карты

    def end_turn(self):
        # 1. Завершение хода игрока (сброс карт)
        self.player.discard_hand()
        
        # 2. Ход противника
        if self.enemy and self.enemy.current_hp > 0:
            self.enemy.take_turn(self.player)
        
        # 3. Начало нового хода (сброс брони, восстановление энергии, добор карт)
        self.player.start_turn()