# Объявление констант, определяющих работу игр
START_MUSIC = True  # Если не нужна музыка на стартовом экране - False
SIZE = WIDTH, HEIGHT = 1200, 800  # Большое разрешение экрана лучше не ставить
FPS = 120
SOUND_DIR = 'sounds'
LOAD_DIR = 'data'
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255),
          'white': (255, 255, 255),
          'green': (102, 204, 0),
          'orange': (255, 102, 51),
          'dark green': (0, 102, 0),
          'black': (12, 12, 12),
          'grey': (52, 52, 52),
          'light-red': (255, 0, 0),
          'dark-blue': (0, 0, 255)}  # Цвета, используемые в играх

WIN_SOUND = 'win.mp3'
ICON_IMAGE = 'game-controller.png'

# Константы для игры в крестики-нолики
TTT_CLICK_SOUND = 'click.mp3'
TTT_CELL_SIZE = WIDTH // 10
TTT_CROSS_IMAGE = 'cross.png'
TTT_NOUGHT_IMAGE = 'nought.png'


# Константы для игры в Аэро хоккей
AH_STICK_RADIUS = 40
AH_STICK_SPEED = 400
AH_STICK_MASS = 2000
AH_PUCK_RADIUS = 30
AH_PUCK_SPEED = 1000  # Рекомендуется задавать начальную скорость не равную нулю во избежание нечестной игры
AH_PUCK_MASS = 500
AH_FRICTION = 0.998
AH_SPEED_LIMIT = 1500
AH_STICK1X = 20
AH_STICK1Y = HEIGHT // 2
AH_STICK2X = WIDTH - 20
AH_STICK2Y = HEIGHT // 2
AH_GOAL_WIDTH = 180
AH_GOAL_Y1 = HEIGHT // 2 - AH_GOAL_WIDTH // 2
AH_GOAL_Y2 = HEIGHT // 2 + AH_GOAL_WIDTH // 2
AH_STICK1_COLOR = COLORS['red']
AH_STICK2_COLOR = COLORS['blue']
AH_FIELD_COLOR = COLORS['white']
AH_PUCK_COLOR = COLORS['black']
AH_BORDER_COLOR = COLORS['black']
AH_GOAL_COLOR = COLORS['orange']
AH_DIVIDING_LINE_COLOR = COLORS['light-red']
AH_GOAL_SOUND = 'goal.mp3'
AH_HIT_SOUND = 'hit.mp3'

# Константы для игры в морской бой
SB_CELL_SIZE = WIDTH // 20
SB_CD_LENGTH = FPS * 2  # Время "перезарядки" после хода одного из игроков
SB_FONT_COLOR = COLORS['dark-blue']
SB_PLAYER1_FILENAME = 'SB_player1.txt'
SB_PLAYER2_FILENAME = 'SB_player2.txt'
SB_EXPLOSION_SOUND = 'SB_explosion.mp3'
SB_MISS_SOUND = 'SB_miss.mp3'
SB_BACKGROUND_IMAGE = 'SB_back.png'
