import sys
import pygame
import pygame_gui
from constants import *  # Переносит все константы, использующиеся в проекте
from TicTacToe import TicTacToeBoard
from AirHockey import Stick, Puck, AirHockey
from SeaBattle import SeaBattleBoard
from load_image import load_image
from load_sound import load_sound

# Начало работы с pygame
#Здесь инициализируются основные параметры Pygame, такие как окно, иконка, часы и менеджер GUI.
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_icon(load_image(ICON_IMAGE))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE, 'style.json')

# Настройка игры в Аэро Хоккей
AH_stick1 = Stick(AH_STICK1_COLOR, AH_STICK1X, AH_STICK1Y)
AH_stick2 = Stick(AH_STICK2_COLOR, AH_STICK2X, AH_STICK2Y)
AH_puck = Puck(AH_PUCK_COLOR, WIDTH // 2, HEIGHT // 2)
AH = AirHockey(screen, AH_FIELD_COLOR, AH_stick1, AH_stick2, AH_puck)

# Настройка игры в Морской Бой
SB = SeaBattleBoard(screen)
SB.set_view((WIDTH - 8 * SB_CELL_SIZE) // 2,
            (HEIGHT - 8 * SB_CELL_SIZE) // 2, SB_CELL_SIZE)

# Настройка игры в крестики нолики
TicTacToe = TicTacToeBoard(screen)
TicTacToe.set_view((WIDTH - TicTacToe.width * TTT_CELL_SIZE) // 2,
                   (HEIGHT - TicTacToe.height * TTT_CELL_SIZE) // 2, TTT_CELL_SIZE)


# Настройка выпадающего списка
# Для добавления новой игры необходимо добавить в словарь ее название и класс
# Также игра должна иметь методы render() и restart()
# Обработку действий в игре можно написать в ф-ии play_game(), если игра статичная
# Если игра требует частых обновлений и проверок, то лучше написать в основной игровой цикл
class InfoScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.caption = "Information"
        self.info_text = [
            "MiniGames",
            "Проект включает в себя 3 игры для двух игроков",
            "на одном экране: аэрохоккей, морской бой, крестики-нолики",
            "Управление в аэрохоккей: WASD - для первого игрока, стрелочки - для второго игрока",
            "Управление в морской бой и крестики-нолики: левой кнопкой мыши",
            "Нажмите SPACE для перезапуска игры",
            "Авторы:",
            "Севрюков Кирилл Евгеньевич, Климачев Сергей Александрович"
        ]
        # Цвета текста и фона
        self.text_color = (0, 0, 0)  # черный
        self.background_color = (255, 255, 255)  # белый

    def render(self):
        self.screen.fill(self.background_color)
        text_y = 100
        for line in self.info_text:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, text_y))
            self.screen.blit(text_surface, text_rect)
            text_y += 40

    def restart(self):
        pass  # Нет необходимости перезапускать информационный экран
# Обновленный словарь с добавленным InfoScreen
games_dict = {'Air Hockey (Аэрохоккей)': AH,
              'Sea Battle (Морской Бой)': SB,
              'Tic Tac Toe (Крестики-нолики)': TicTacToe,
              'О программе': InfoScreen(screen)}

game_changer = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=list(games_dict.keys()),
    starting_option='Air Hockey (Аэрохоккей)',
    manager=manager,
    relative_rect=pygame.Rect((10, 10), (400, 50))
)


def play_game(game, event):
    """Обрабатка ивентов некоторых игр"""
    if game == TicTacToe or game == SB:
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.get_click(event.pos)
    elif game == TicTacToe or game == SB:  # Добавлено условие для TicTacToe и SB
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.get_click(event.pos)


def terminate():
    """Завершение всех процессов и выход из программы"""
    pygame.quit()
    sys.exit()


def start_screen():
    """Запуск стартового экрана (заставки)"""
    fon = pygame.transform.scale(load_image('start_screen.png'), (WIDTH, HEIGHT))
    pygame.display.set_caption('Pygame Mini Games')
    screen.blit(fon, (0, 0))
    if START_MUSIC:
        pygame.mixer.Sound.play(load_sound('start.mp3'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.stop()
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    """Запуск игры"""
    game = AH
    while True:
        time_delta = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            play_game(game, event)
            if event.type == pygame.KEYDOWN:
                # Перезапуск любой игры осуществляется через пробел
                if event.key == pygame.K_SPACE:
                    game.restart()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    game.restart()
                    game = games_dict[event.text]
            manager.process_events(event)
        if game == AH:
            keys = pygame.key.get_pressed()
            # Проверка кнопок Игрока 1
            w = keys[pygame.K_w]
            s = keys[pygame.K_s]
            d = keys[pygame.K_d]
            a = keys[pygame.K_a]
            # Проверка кнопок Игрока 2
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            right = keys[pygame.K_RIGHT]
            left = keys[pygame.K_LEFT]
            # Перемещение Игрока 1
            AH_stick1.move(w, s, a, d, time_delta)
            AH_stick1.check_vertical()
            AH_stick1.check_left()
            # Перемещение Игрока 2
            AH_stick2.move(up, down, left, right, time_delta)
            AH_stick2.check_vertical()
            AH_stick2.check_right()
            # Перемещение шайбы
            AH_puck.move(time_delta)
            if game.goal():  # Если шайба попала в ворота - перезапуск игры
                pygame.mixer.Sound.play(AirHockey.goal_sound)
                game.restart()
            AH_puck.check()
            if AH_puck.check_collision(AH_stick1):  # Отскоки
                pygame.mixer.Sound.play(AirHockey.hit_sound)
            if AH_puck.check_collision(AH_stick2):  # Отскоки
                pygame.mixer.Sound.play(AirHockey.hit_sound)
        pygame.display.set_caption(game.caption)
        screen.fill((0, 0, 0))
        manager.update(time_delta)
        game.render()
        manager.draw_ui(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    start_game()
