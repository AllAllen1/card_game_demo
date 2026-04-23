class Enemy:
    def __init__(self, name="Гоблин-разбойник", hp=25, damage=6):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.damage = damage
        self.armor = 0

    def take_turn(self, player):
        damage_to_deal = self.damage
        
        # Урон сначала поглощается броней
        if player.armor > 0:
            blocked = min(player.armor, damage_to_deal)
            player.armor -= blocked
            damage_to_deal -= blocked
            
        # Остаток урона идет в здоровье
        player.current_hp -= damage_to_deal