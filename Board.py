import pygame


class Board:
    """Класс, использующийся для игр на клетчатом поле"""
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.screen = screen

    def correct(self, x, y):
        """Проверка корректности данных коордиант"""
        return True if 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1 else False

    def set_view(self, left, top, cell_size):
        """Устанавливает отступы слева и сверху, а также размер клетки поля"""
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        """Прорисовка поля"""
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                x += self.cell_size
            y += self.cell_size

    def get_cell(self, mouse_pos):
        """Возвращает координаты клетки поля, которой соответствуют координаты мыши mouse_pos"""
        x, y = mouse_pos
        board_size_x = self.left + self.cell_size * self.width
        board_size_y = self.top + self.cell_size * self.height
        if self.left > x or x > board_size_x or self.top > y or y > board_size_y:
            return None
        return self.width - 1 - (board_size_x - x) // self.cell_size, self.height - 1 - (
                board_size_y - y) // self.cell_size

    def on_click(self, cell):
        """Метод для выполнения каких-то действий для данной клетки"""
        pass

    def get_click(self, mouse_pos):
        """Метод-посредник для обработки нажатия пользователя и последующего дейсвтия"""
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
