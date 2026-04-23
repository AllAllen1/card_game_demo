from player import Player
from enemy import Goblin, Skeleton

class Game:
    def __init__(self, num_enemies=1):
        self.player = Player()
        self.enemies = []
        self.enemies.append(Goblin())
        if num_enemies == 2:
            self.enemies.append(Skeleton())
            
        # Выдаем стартовую руку при начале игры
        self.player.draw_cards(5)
        self.current_room = None
        # Здесь в будущем будет инициализация колоды и карты

    def end_turn(self):
        # 1. Завершение хода игрока (сброс карт)
        self.player.discard_hand()
        
        # 2. Ход противника
        for enemy in self.enemies:
            if enemy.current_hp > 0:
                enemy.take_turn(self.player)
        
        # 3. Начало нового хода (сброс брони, восстановление энергии, добор карт)
        self.player.start_turn()