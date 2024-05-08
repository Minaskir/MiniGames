import pygame
from Board import Board
from load_image import load_image
from load_sound import load_sound
from constants import WIN_SOUND, TTT_CLICK_SOUND, COLORS, WIDTH, HEIGHT, TTT_NOUGHT_IMAGE, TTT_CROSS_IMAGE

size = width, height = 800, 800
screen = pygame.display.set_mode(size)


class TicTacToeBoard(Board):
    """Класс для игры в Крестики-нолики"""
    cross = load_image(TTT_CROSS_IMAGE)
    nought = load_image(TTT_NOUGHT_IMAGE)
    press_sound = load_sound(TTT_CLICK_SOUND)
    win_sound = load_sound(WIN_SOUND)

    def __init__(self, screen):
        super().__init__(3, 3, screen)
        self.turn = 'red'
        self.outline = self.cell_size // 10
        self.cross = pygame.transform.scale(TicTacToeBoard.cross,
                                            (self.cell_size - self.outline, self.cell_size - self.outline))
        self.nought = pygame.transform.scale(TicTacToeBoard.nought,
                                             (self.cell_size - self.outline, self.cell_size - self.outline))
        self.working = True
        self.won = None
        self.draw = False
        self.caption = 'Крестики-нолики'
        self.won_cells = ()

    def set_view(self, left, top, cell_size):
        """Устанавливает отступы слева и сверху, размер клетки поля, толщину границ клеток"""
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.outline = self.cell_size // 10
        self.cross = pygame.transform.scale(TicTacToeBoard.cross,
                                            (self.cell_size - self.outline, self.cell_size - self.outline))
        self.nought = pygame.transform.scale(TicTacToeBoard.nought,
                                             (self.cell_size - self.outline, self.cell_size - self.outline))

    def render(self):
        """Прорисовка поля"""
        self.screen.fill(COLORS[self.turn])
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                pygame.draw.rect(self.screen, COLORS[self.turn],
                                 (x, y, self.cell_size, self.cell_size), self.outline)
                if x != self.left:
                    pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y + self.cell_size),
                                     self.outline)  # Рисует поле
                if self.board[i][j] == 1:  # Рисует крестик
                    self.screen.blit(self.cross, (x + self.outline // 2, y + self.outline // 2))
                if self.board[i][j] == 2:  # Рисует нолик
                    self.screen.blit(self.nought, (x + self.outline // 2, y + self.outline // 2))
                x += self.cell_size
            if y != self.top:
                pygame.draw.line(self.screen, (0, 0, 0), (self.left, y),
                                 (self.left + self.cell_size * self.width, y), self.outline)
            y += self.cell_size
        if self.won:
            self.set_win()
        if self.draw:
            self.set_draw()

    def check_three(self, p1, p2, p3):
        """Проверка трех клеток, расположенных подряд (вызывается из check_win())"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        # Если равны, то есть победитель
        if self.board[y1][x1] == self.board[y2][x2] == self.board[y3][x3] != 0:
            self.working = False
            self.won = 'red' if self.board[y1][x1] == 1 else 'blue'
            pygame.mixer.Sound.play(TicTacToeBoard.win_sound)
            self.won_cells = (p1, p3)

    def check_win(self):
        """Проверка победителя или ничьи (все возможные комбинации)"""
        c = 0
        for i in range(3):
            self.check_three((i, 0), (i, 1), (i, 2))
            self.check_three((0, i), (1, i), (2, i))
        self.check_three((0, 0), (1, 1), (2, 2))
        self.check_three((2, 0), (1, 1), (0, 2))
        for i in range(3):
            if all(j for j in self.board[i]):
                c += 1
        if c == 3 and not self.won:  # Ничья
            self.set_draw()

    def set_draw(self):
        """Установка ничьи"""
        self.draw = True
        self.turn = 'white'
        self.caption = 'Крестики-нолики (НИЧЬЯ)'

    def on_click(self, cell):
        """Совершает действие по нажатию кнопки мыши пользователем"""
        if cell:
            x, y = cell
            if not self.board[y][x]:
                if self.working:
                    pygame.mixer.Sound.play(TicTacToeBoard.press_sound)
                    self.board[y][x] = 1 if self.turn == 'red' else 2
                self.check_win()
                if self.working:
                    self.turn = 'blue' if self.turn == 'red' else 'red'

    def set_win(self):
        """Прорисовка линий элементов, образующих ряд из трех"""
        x1, y1 = self.won_cells[0]
        x2, y2 = self.won_cells[1]
        if x1 == x2 and y1 != y2:
            x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size + self.cell_size // 2
            x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size // 2
            y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
            y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
        elif x1 != x2 and y1 == y2:
            x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size
            x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size
            y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size + self.cell_size // 2
            y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size // 2
        elif x1 != x2 and y1 != y2 and x2 > x1:
            x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size
            x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size
            y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
            y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
        else:
            x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size + self.cell_size
            x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size
            y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
            y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
        pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), self.outline)
        self.caption = f'Крестики-нолики ({self.won.upper()} ПОБЕДИЛ!)'

    def restart(self):
        """Перезапуск игры"""
        self.won = None
        self.working = True
        self.board = [[0] * self.width for _ in range(self.height)]
        self.turn = 'red'
        self.caption = 'Крестики-нолики'
