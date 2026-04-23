class Entity:
    def __init__(self, name, hp):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0