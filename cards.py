import os
# Для работы этого кода убедись, что установлена библиотека: pip install pygame
import pygame

class Card:
    # Общий кэш для всех карт, чтобы не загружать одну и ту же картинку с диска много раз
    _image_cache = {}

    def __init__(self, name: str, energy_cost: int, image_filename: str):
        self.name = name
        self.cost = energy_cost
        
        # Формируем путь к картинке в папке cards_png
        image_path = os.path.join("cards_png", image_filename)
        
        # Проверяем, загружали ли мы эту картинку ранее
        if image_path not in Card._image_cache:
            try:
                # Загружаем изображение и масштабируем
                image = pygame.image.load(image_path)
                Card._image_cache[image_path] = pygame.transform.scale(image, (100, 150))
            except FileNotFoundError:
                print(f"Внимание: Изображение {image_path} не найдено. Используется заглушка.")
                # Создаем прямоугольник-заглушку
                placeholder = pygame.Surface((100, 150))
                placeholder.fill((100, 100, 100)) # Серый цвет
                Card._image_cache[image_path] = placeholder
                
        # Берем готовую картинку из кэша
        self.image = Card._image_cache[image_path]

    def draw(self, surface, x: int, y: int):
        """Отрисовывает карту на переданной поверхности (экране) в координатах x, y"""
        surface.blit(self.image, (x, y))

class AttackCard(Card):
    def __init__(self):
        # Укажи точное имя файла твоей картинки для атаки, например "attack.png"
        super().__init__(name="Удар", energy_cost=1, image_filename="attack.png")
        self.damage = 6

    def play(self, player, target):
        target.take_damage(self.damage)

class DefenseCard(Card):
    def __init__(self):
        # Укажи точное имя файла твоей картинки для защиты, например "defense.png"
        super().__init__(name="Блок", energy_cost=1, image_filename="defense.png")
        self.block = 5

    def play(self, player, target):
        player.armor += self.block