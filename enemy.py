from entities import Entity

class Enemy(Entity):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp)
        self.damage = damage

    def take_turn(self, player):
        damage_to_deal = self.damage
        
        # Урон сначала поглощается броней
        if player.armor > 0:
            blocked = min(player.armor, damage_to_deal)
            player.armor -= blocked
            damage_to_deal -= blocked
            
        # Остаток урона идет в здоровье
        player.current_hp -= damage_to_deal

class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Гоблин-разбойник", hp=25, damage=6)

class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Скелет", hp=20, damage=5)