from pathlib import Path
import random
import pygame
from attitude.game_object import GameObject


# heal類別
class Heal(GameObject):
    # 全域、靜態變數
    heal_effect = []
    # 建構式
    def __init__(self, xy=None):
        GameObject.__init__(self)
        if xy is None:
            self._y = -100
            self._x = random.randint(10, self._playground[0] - 100)
        else:
            self._x = xy[0]  # 座標屬性
            self._y = xy[1]  #

        if Heal.heal_effect:
            pass
        else:
            __parent_path = Path(__file__).parents[1]
            icon_path = __parent_path / 'res' / 'cure_small.png'
            Heal.heal_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'cure_medium.png'
            Heal.heal_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'cure_large.png'
            Heal.heal_effect.append(pygame.image.load(icon_path))

        self.__image_index = 0
        self._image = Heal.heal_effect[self.__image_index]
        self.__fps_count = 0

    def update(self):
        self.__fps_count += 1
        if self.__fps_count > 20:
            self.__image_index += 1
            if self.__image_index >= 3:
                self._available = False
            else:
                self._image = Heal.heal_effect[self.__image_index]
