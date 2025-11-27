import pygame
import sys
import os
from game import Game

class PygameApp:
    def __init__(self):
        """Инициализация Pygame и создание окна"""
        # Инициализация Pygame
        pygame.init()
        
        # Настройки окна
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # Цвета
        self.BG_COLOR = (30, 30, 40)  # Темно-синий
        self.TEXT_COLOR = (220, 220, 220)
        self.BUTTON_COLOR = (70, 130, 180)  # Steel blue
        self.BUTTON_HOVER_COLOR = (100, 160, 210)
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Deck - Карточный рогалик")
        
        # Шрифты
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 36)
        self.debug_font = pygame.font.Font(None, 24)
        
        # Игровые объекты
        self.game = None
        self.current_state = "main_menu"  # main_menu, playing, game_over
        self.clock = pygame.time.Clock()
        
        # Кнопки меню
        self.menu_buttons = [
            {"text": "Новая игра", "rect": pygame.Rect(0, 0, 300, 50), "action": "start_game"},
            {"text": "Выход", "rect": pygame.Rect(0, 0, 300, 50), "action": "quit"}
        ]
        self._position_buttons()
    
    def _position_buttons(self):
        """Позиционирование кнопок меню по центру"""
        button_width = 300
        button_height = 50
        button_spacing = 20
        total_height = len(self.menu_buttons) * button_height + (len(self.menu_buttons) - 1) * button_spacing
        start_y = (self.SCREEN_HEIGHT - total_height) // 2
        
        for i, button in enumerate(self.menu_buttons):
            button["rect"] = pygame.Rect(
                (self.SCREEN_WIDTH - button_width) // 2,
                start_y + i * (button_height + button_spacing),
                button_width,
                button_height
            )
    
    def handle_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.handle_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == "playing":
                        self.current_state = "main_menu"
                    else:
                        return False
                elif event.key == pygame.K_F1:
                    self.toggle_debug()
        
        return True
    
    def handle_click(self, mouse_pos):
        """Обработка кликов мыши"""
        if self.current_state == "main_menu":
            for button in self.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.execute_button_action(button["action"])
        
        elif self.current_state == "playing":
            # Здесь будет логика кликов в игре (по картам и т.д.)
            pass
    
    def execute_button_action(self, action):
        """Выполнение действия кнопки"""
        if action == "start_game":
            self.start_new_game()
        elif action == "quit":
            pygame.quit()
            sys.exit()
    
    def start_new_game(self):
        """Начало новой игры"""
        self.game = Game()
        self.current_state = "playing"
        print("Новая игра начата!")
    
    def toggle_debug(self):
        """Переключение режима отладки"""
        # Можно добавить отладочную информацию
        pass
    
    def draw_main_menu(self):
        """Отрисовка главного меню"""
        # Фон
        self.screen.fill(self.BG_COLOR)
        
        # Заголовок
        title_surface = self.title_font.render("DUNGEON DECK", True, (255, 215, 0))  # Золотой
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surface, title_rect)
        
        # Подзаголовок
        subtitle_surface = self.menu_font.render("Карточный рогалик", True, self.TEXT_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            # Определяем цвет кнопки (ховер или обычный)
            color = self.BUTTON_HOVER_COLOR if button["rect"].collidepoint(mouse_pos) else self.BUTTON_COLOR
            
            # Рисуем кнопку
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2, border_radius=10)
            
            # Текст кнопки
            text_surface = self.menu_font.render(button["text"], True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
        
        # Футер
        footer_text = "Нажмите F1 для отладки | ESC для выхода"
        footer_surface = self.debug_font.render(footer_text, True, (150, 150, 150))
        footer_rect = footer_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(footer_surface, footer_rect)
    
    def draw_playing_screen(self):
        """Отрисовка игрового экрана"""
        # Фон игровой области
        self.screen.fill(self.BG_COLOR)
        
        # Верхняя панель (здоровье, мана и т.д.)
        self.draw_game_ui()
        
        # Область противника
        self.draw_enemy_area()
        
        # Рука игрока (карты)
        self.draw_player_hand()
        
        # Нижняя панель (логи, кнопки)
        self.draw_action_panel()
    
    def draw_game_ui(self):
        """Отрисовка игрового UI"""
        if not self.game:
            return
        
        # Панель статуса игрока
        panel_rect = pygame.Rect(20, 20, self.SCREEN_WIDTH - 40, 80)
        pygame.draw.rect(self.screen, (50, 50, 60), panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 120), panel_rect, 2, border_radius=8)
        
        # Здоровье
        hp_text = f"HP: {self.game.player.current_hp}/{self.game.player.max_hp}"
        hp_surface = self.menu_font.render(hp_text, True, (255, 100, 100))
        self.screen.blit(hp_surface, (40, 40))
        
        # Мана
        mana_text = f"Мана: {self.game.player.current_mana}/{self.game.player.max_mana}"
        mana_surface = self.menu_font.render(mana_text, True, (100, 150, 255))
        self.screen.blit(mana_surface, (200, 40))
        
        # Броня
        armor_text = f"Броня: {self.game.player.armor}"
        armor_surface = self.menu_font.render(armor_text, True, (200, 200, 100))
        self.screen.blit(armor_surface, (400, 40))
    
    def draw_enemy_area(self):
        """Отрисовка области противника"""
        enemy_rect = pygame.Rect(100, 120, self.SCREEN_WIDTH - 200, 150)
        pygame.draw.rect(self.screen, (60, 60, 70), enemy_rect, border_radius=10)
        pygame.draw.rect(self.screen, (120, 120, 140), enemy_rect, 2, border_radius=10)
        
        # Заглушка - потом заменим на реального врага
        enemy_text = self.menu_font.render("Противник появится здесь", True, self.TEXT_COLOR)
        enemy_text_rect = enemy_text.get_rect(center=enemy_rect.center)
        self.screen.blit(enemy_text, enemy_text_rect)
    
    def draw_player_hand(self):
        """Отрисовка руки игрока (карт)"""
        hand_area = pygame.Rect(50, 400, self.SCREEN_WIDTH - 100, 250)
        pygame.draw.rect(self.screen, (40, 40, 50), hand_area, border_radius=8)
        
        # Заглушка для карт
        card_text = self.menu_font.render("Карты игрока появятся здесь", True, self.TEXT_COLOR)
        card_text_rect = card_text.get_rect(center=hand_area.center)
        self.screen.blit(card_text, card_text_rect)
        
        # Временное отображение карт (если они есть)
        if self.game and hasattr(self.game.player, 'hand'):
            for i, card in enumerate(self.game.player.hand):
                self.draw_card(card, 150 + i * 120, 450)
    
    def draw_card(self, card, x, y):
        """Отрисовка одной карты"""
        card_rect = pygame.Rect(x, y, 100, 150)
        
        # Основа карты
        pygame.draw.rect(self.screen, (240, 240, 240), card_rect, border_radius=5)
        pygame.draw.rect(self.screen, (50, 50, 50), card_rect, 2, border_radius=5)
        
        # Название карты
        name_surface = self.debug_font.render(card.name, True, (0, 0, 0))
        self.screen.blit(name_surface, (x + 5, y + 10))
        
        # Стоимость маны
        cost_bg = pygame.Rect(x + 5, y + 5, 20, 20)
        pygame.draw.rect(self.screen, (30, 100, 200), cost_bg, border_radius=10)
        cost_text = self.debug_font.render(str(card.cost), True, (255, 255, 255))
        cost_rect = cost_text.get_rect(center=cost_bg.center)
        self.screen.blit(cost_text, cost_rect)
    
    def draw_action_panel(self):
        """Отрисовка панели действий"""
        action_rect = pygame.Rect(20, self.SCREEN_HEIGHT - 80, self.SCREEN_WIDTH - 40, 60)
        pygame.draw.rect(self.screen, (50, 50, 60), action_rect, border_radius=8)
        
        # Кнопка завершения хода
        end_turn_rect = pygame.Rect(self.SCREEN_WIDTH - 150, self.SCREEN_HEIGHT - 70, 120, 40)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, end_turn_rect, border_radius=5)
        end_text = self.menu_font.render("Завершить ход", True, self.TEXT_COLOR)
        end_rect = end_text.get_rect(center=end_turn_rect.center)
        self.screen.blit(end_text, end_rect)
    
    def draw_game_over(self):
        """Отрисовка экрана завершения игры"""
        self.screen.fill((20, 20, 30))
        
        game_over_text = self.title_font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
        text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        score_text = self.menu_font.render("Нажмите ESC для возврата в меню", True, self.TEXT_COLOR)
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(score_text, score_rect)
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        print("Pygame приложение запущено!")
        
        while running:
            # Обработка событий
            running = self.handle_events()
            
            # Отрисовка в зависимости от состояния
            if self.current_state == "main_menu":
                self.draw_main_menu()
            elif self.current_state == "playing":
                self.draw_playing_screen()
            elif self.current_state == "game_over":
                self.draw_game_over()
            
            # Обновление экрана
            pygame.display.flip()
            
            # Контроль FPS
            self.clock.tick(self.FPS)
        
        # Завершение работы
        pygame.quit()
        sys.exit()

def main():
    """Точка входа в программу"""
    try:
        app = PygameApp()
        app.run()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()