# Первый игрок перемещается кнопками WASD, второй стрелочками

from load_sound import load_sound
import pygame
import math
import constants as cn

pygame.init()
screen = pygame.display.set_mode(cn.SIZE)
clock = pygame.time.Clock()


class AirHockey:
    """Класс для игры в Аэро Хоккей"""

    goal_sound = load_sound(cn.AH_GOAL_SOUND)
    hit_sound = load_sound(cn.AH_HIT_SOUND)

    def __init__(self, screen, color, stick1, stick2, puck):
        self.screen = screen
        self.color = color
        self.s1 = stick1
        self.s2 = stick2
        self.puck = puck
        self.caption = 'Аэрохоккей'

    def render(self):
        """Прорисовка поля для игры, клюшек и шайбы"""
        self.screen.fill(self.color)
        # Границы поля
        pygame.draw.rect(self.screen, cn.AH_BORDER_COLOR, (0, 0, cn.WIDTH, cn.HEIGHT), 15)
        # Ворота
        pygame.draw.line(self.screen, cn.COLORS['red'], (0, cn.AH_GOAL_Y1),
                         (0, cn.AH_GOAL_Y1 + cn.AH_GOAL_WIDTH), 15)
        pygame.draw.line(self.screen, cn.COLORS['blue'], (cn.WIDTH - 1, cn.AH_GOAL_Y1),
                         (cn.WIDTH - 1, cn.AH_GOAL_Y1 + cn.AH_GOAL_WIDTH), 15)
        # Разделяющая полоса
        pygame.draw.line(self.screen, cn.AH_DIVIDING_LINE_COLOR, (cn.WIDTH // 2, 10),
                         (cn.WIDTH // 2, cn.HEIGHT - 10), 5)
        # Прорисовка клюшек и шайбы
        self.s1.draw(self.screen)
        self.s2.draw(self.screen)
        self.puck.draw(self.screen)

    def restart(self):
        """Перезапуск игры"""
        self.puck.reset()
        self.s1.reset(cn.AH_STICK1X, cn.AH_STICK1Y)
        self.s2.reset(cn.AH_STICK2X, cn.AH_STICK2Y)

    def goal(self):
        """Проверка на попадание в ворота"""
        return ((self.puck.x - self.puck.radius <= 0)
                and (self.puck.y >= cn.AH_GOAL_Y1)
                and (self.puck.y <= cn.AH_GOAL_Y2)) \
               or ((self.puck.x + self.puck.radius >= cn.WIDTH)
                   and (self.puck.y >= cn.AH_GOAL_Y1) and (self.puck.y <= cn.AH_GOAL_Y2))


class Stick:
    """Класс для клюшки в игре Аэро Хоккей"""

    def __init__(self, color, x, y):
        self.x = x
        self.color = color
        self.y = y
        self.radius = cn.AH_STICK_RADIUS
        self.speed = cn.AH_STICK_SPEED
        self.mass = cn.AH_STICK_MASS
        self.angle = 0

    def check_vertical(self):
        """Проверка выхода за границы экрана сверху и снизу"""
        if self.y - self.radius <= 0:
            self.y = self.radius
        elif self.y + self.radius > cn.HEIGHT:
            self.y = cn.HEIGHT - self.radius

    def check_left(self):
        """Проверка для левой клюшки"""
        if self.x - self.radius <= 0:
            self.x = self.radius
        elif self.x + self.radius > cn.WIDTH // 2:
            self.x = cn.WIDTH // 2 - self.radius

    def check_right(self):
        """Проверка для правой клюшки"""
        if self.x + self.radius > cn.WIDTH:
            self.x = cn.WIDTH - self.radius
        elif self.x - self.radius < cn.WIDTH // 2:
            self.x = cn.WIDTH // 2 + self.radius

    def draw(self, screen):
        """Прорисовка клюшки на экране"""
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.color, pos, self.radius, 0)
        pygame.draw.circle(screen, (0, 0, 0), pos, self.radius, 5)
        pygame.draw.circle(screen, (0, 0, 0), pos, self.radius - 10, 5)

    def reset(self, x, y):
        """Установление новой позиции для клюшки"""
        self.x = x
        self.y = y

    def move(self, up, down, left, right, time):
        """Перемещение клюшки по полю"""
        dx, dy = self.x, self.y
        self.x += (right - left) * self.speed * time
        self.y += (down - up) * self.speed * time
        dx, dy = self.x - dx, self.y - dy
        self.angle = math.atan2(dy, dx)


class Puck:
    """Класс для шайбы в игре Аэро Хоккей"""

    def __init__(self, color, x, y):
        self.x, self.y = x, y
        self.color = color
        self.radius = cn.AH_PUCK_RADIUS
        self.speed = cn.AH_PUCK_SPEED
        self.mass = cn.AH_PUCK_MASS
        self.angle = 0

    def move(self, time):
        """Перемещение шайбу по полю"""
        self.x += math.sin(self.angle) * self.speed * time
        self.y -= math.cos(self.angle) * self.speed * time

        self.speed *= cn.AH_FRICTION

    def reset(self):
        """Перемещение шайбы обратно в центр поля"""
        self.angle = 0
        self.speed = cn.AH_PUCK_SPEED
        self.x = cn.WIDTH // 2
        self.y = cn.HEIGHT // 2

    def check(self):
        """Проверка выхода шайбы за границы поля"""
        if self.x + self.radius > cn.WIDTH:
            self.x = 2 * (cn.WIDTH - self.radius) - self.x
            self.angle = -self.angle
        elif self.x - self.radius < 0:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        if self.y + self.radius > cn.HEIGHT:
            self.y = 2 * (cn.HEIGHT - self.radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y - self.radius < 0:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle

    @staticmethod
    def add_vector(angle1, len1, angle2, len2):
        """Создание вектора для движения шайбы"""
        x = math.sin(angle1) * len1 + math.sin(angle2) * len2
        y = math.cos(angle1) * len1 + math.cos(angle2) * len2
        len0 = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return angle, len0

    def check_collision(self, stick):
        """Проверка на столкновение с клюшками"""
        dx = self.x - stick.x
        dy = self.y - stick.y
        distance = math.hypot(dx, dy)  # Расстояние между центрами окружностей клюшки и шайбы
        if distance > self.radius + stick.radius:
            return False  # Столкновения нет

        # Рассчет угла отражения
        tan = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tan
        total_mass = self.mass + stick.mass

        vector1 = (self.angle, self.speed * (self.mass - stick.mass) / total_mass)
        vector2 = (temp_angle, 2 * stick.speed * stick.mass / total_mass)

        (self.angle, self.speed) = self.add_vector(*vector1, *vector2)

        self.speed = min(self.speed, cn.AH_SPEED_LIMIT)  # Скорость не должна быть выше максимальной

        vector1 = (stick.angle, stick.speed * (stick.mass - self.mass) / total_mass)
        vector2 = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = stick.speed
        stick.angle, stick.speed = self.add_vector(*vector1, *vector2)
        stick.speed = temp_speed

        # Во избежание "прилипания" клюшек и шайбы
        offset = 0.5 * (self.radius + stick.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        stick.x -= math.sin(temp_angle) * offset
        stick.y += math.cos(temp_angle) * offset
        return True

    def draw(self, screen):
        """Прорисовка шайбы на экране"""
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.color, pos, self.radius)
        pygame.draw.circle(screen, cn.COLORS['grey'], pos, self.radius - 10)
