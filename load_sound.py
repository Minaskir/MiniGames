import os
import sys
import pygame
from constants import SOUND_DIR

pygame.init()


def load_sound(name):
    """Загрузка звука из директории constants.SOUND_DIR"""
    fullname = os.path.join(SOUND_DIR, name)
    if not os.path.isfile(fullname):
        print(f'Файл с названием {name} не найден')
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound
