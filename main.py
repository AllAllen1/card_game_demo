import pygame
import sys
import os
from game import Game
from save_manager import save_game, load_game, has_save

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
        self.current_state = "main_menu"  # main_menu, playing, game_over, victory
        self.clock = pygame.time.Clock()
        
        # Кнопки UI в игре
        self.end_turn_rect = pygame.Rect(self.SCREEN_WIDTH - 150, self.SCREEN_HEIGHT - 70, 120, 40)
        
        # Кнопки меню
        self.menu_buttons = [
            {"text": "Играть (1 враг)", "rect": pygame.Rect(0, 0, 300, 50), "action": "start_game_1"},
            {"text": "Играть (2 врага)", "rect": pygame.Rect(0, 0, 300, 50), "action": "start_game_2"},
            {"text": "Выход", "rect": pygame.Rect(0, 0, 300, 50), "action": "quit"}
        ]
        if has_save():
            self.menu_buttons.insert(0, {"text": "Загрузить игру", "rect": pygame.Rect(0, 0, 300, 50), "action": "load_game"})
        self._position_buttons()

        # Уведомление на экране
        self._notification_text = ""
        self._notification_timer = 0
    
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
                    if self.current_state in ["playing", "game_over", "victory"]:
                        self.current_state = "main_menu"
                    else:
                        return False
                elif event.key == pygame.K_F1:
                    self.toggle_debug()
                elif event.key == pygame.K_F5:
                    if self.current_state == "playing" and self.game:
                        save_game(self.game, self.current_state)
                        self._show_notification("Игра сохранена!")
                elif event.key == pygame.K_F9:
                    result = load_game()
                    if result:
                        self.game, self.current_state = result
                        self._show_notification("Игра загружена!")
        
        return True
    
    def handle_click(self, mouse_pos):
        """Обработка кликов мыши"""
        if self.current_state == "main_menu":
            for button in self.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.execute_button_action(button["action"])
        
        elif self.current_state == "playing":
            if self.end_turn_rect.collidepoint(mouse_pos):
                self.game.end_turn()
            elif self.game and hasattr(self.game.player, 'hand'):
                # Проверяем клики по картам
                for i, card in enumerate(self.game.player.hand):
                    # Восстанавливаем хитбокс карты по тем же координатам, что и при отрисовке
                    card_rect = pygame.Rect(150 + i * 120, 450, 100, 150)
                    if card_rect.collidepoint(mouse_pos):
                        self.play_card(card)
                        break
    
    def play_card(self, card):
        """Разыгрывание карты"""
        if self.game.player.current_energy >= card.cost:
            self.game.player.current_energy -= card.cost
            
            # Для простоты: всегда бьем первого живого врага
            target = self.game.enemies[0] if self.game.enemies else None
            card.play(self.game.player, target)
            
            self.game.player.hand.remove(card)
            self.game.player.discard_pile.append(card)
            print(f"Сыграна карта: {card.name}")
            
            # Очистка мертвых врагов
            self.game.enemies = [e for e in self.game.enemies if e.current_hp > 0]
            if not self.game.enemies:
                self.current_state = "victory"
        else:
            print("Недостаточно энергии!")

    
    def execute_button_action(self, action):
        """Выполнение действия кнопки"""
        if action == "start_game_1":
            self.start_new_game(1)
        elif action == "start_game_2":
            self.start_new_game(2)
        elif action == "load_game":
            result = load_game()
            if result:
                self.game, self.current_state = result
                self._show_notification("Игра загружена!")
        elif action == "quit":
            pygame.quit()
            sys.exit()
    
    def start_new_game(self, num_enemies):
        """Начало новой игры"""
        self.game = Game(num_enemies)
        self.current_state = "playing"
        print("Новая игра начата!")
    
    def toggle_debug(self):
        """Переключение режима отладки"""
        pass

    def _show_notification(self, text, duration_ms=2000):
        self._notification_text = text
        self._notification_timer = pygame.time.get_ticks() + duration_ms

    def _draw_notification(self):
        if self._notification_text and pygame.time.get_ticks() < self._notification_timer:
            surf = self.menu_font.render(self._notification_text, True, (255, 255, 100))
            rect = surf.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            bg = rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (30, 30, 30), bg, border_radius=6)
            pygame.draw.rect(self.screen, (255, 255, 100), bg, 2, border_radius=6)
            self.screen.blit(surf, rect)
    
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
        footer_text = "F1 — отладка | ESC — выход"
        footer_surface = self.debug_font.render(footer_text, True, (150, 150, 150))
        footer_rect = footer_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 30))
        self.screen.blit(footer_surface, footer_rect)
    
    def draw_playing_screen(self):
        """Отрисовка игрового экрана"""
        # Фон игровой области
        self.screen.fill(self.BG_COLOR)
        
        # Верхняя панель (здоровье, энергия и т.д.)
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
        
        # Энергия
        energy_text = f"Энергия: {self.game.player.current_energy}/{self.game.player.max_energy}"
        energy_surface = self.menu_font.render(energy_text, True, (255, 200, 50))
        self.screen.blit(energy_surface, (200, 40))
        
        # Броня
        armor_text = f"Броня: {self.game.player.armor}"
        armor_surface = self.menu_font.render(armor_text, True, (200, 200, 100))
        self.screen.blit(armor_surface, (400, 40))
    
    def draw_enemy_area(self):
        """Отрисовка области противника"""
        if not self.game or not hasattr(self.game, 'enemies'):
            return
            
        for i, enemy in enumerate(self.game.enemies):
            enemy_rect = pygame.Rect(100 + i * 350, 120, 300, 150)
            
            # Первый враг считается текущей целью и выделяется красным
            border_color = (255, 50, 50) if i == 0 else (120, 120, 140)
            pygame.draw.rect(self.screen, (60, 60, 70), enemy_rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, enemy_rect, 2, border_radius=10)
            
            name_text = self.menu_font.render(f"{enemy.name} (Атака {enemy.damage})", True, self.TEXT_COLOR)
            self.screen.blit(name_text, (enemy_rect.x + 20, enemy_rect.y + 20))
            
            hp_text = f"HP: {enemy.current_hp}/{enemy.max_hp}"
            hp_surface = self.menu_font.render(hp_text, True, (255, 100, 100))
            self.screen.blit(hp_surface, (enemy_rect.x + 20, enemy_rect.y + 70))
    
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
        
        # Отрисовка картинки карты
        self.screen.blit(card.image, (x, y))
        # Рамка вокруг карты
        pygame.draw.rect(self.screen, (50, 50, 50), card_rect, 2, border_radius=5)
        
        # Название карты
        name_surface = self.debug_font.render(card.name, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (x + 2, y + 125, 96, 22)) # Черная подложка для текста
        self.screen.blit(name_surface, (x + 5, y + 128))
        
        # Стоимость энергии
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
        mouse_pos = pygame.mouse.get_pos()
        color = self.BUTTON_HOVER_COLOR if self.end_turn_rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color, self.end_turn_rect, border_radius=5)
        end_text = self.menu_font.render("Завершить ход", True, self.TEXT_COLOR)
        end_rect = end_text.get_rect(center=self.end_turn_rect.center)
        self.screen.blit(end_text, end_rect)
    
    def _draw_message_screen(self, title_text, title_color, bg_color):
        """Отрисовка экранов с сообщениями (победа/поражение)"""
        self.screen.fill(bg_color)
        
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.menu_font.render("Нажмите ESC для возврата в меню", True, self.TEXT_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(subtitle_surface, subtitle_rect)

    def draw_game_over(self):
        """Отрисовка экрана завершения игры"""
        self._draw_message_screen("ИГРА ОКОНЧЕНА", (255, 100, 100), (20, 20, 30))
    
    def draw_victory(self):
        """Отрисовка экрана победы"""
        self._draw_message_screen("ПОБЕДА!", (100, 255, 100), (20, 40, 20))

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
            elif self.current_state == "victory":
                self.draw_victory()

            self._draw_notification()

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