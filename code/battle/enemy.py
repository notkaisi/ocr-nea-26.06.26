#--enemy.py--
from settings import *
from random import sample

class Attributes:
    def get_data(self, name):
        self.element=enemy_data[name]['element']
        self._health=self.max_health=enemy_data[name]['health']
        self.abilities=sample(list(abilities_data.keys()),4) # samples a random 4 out of the list
        self.name=name
        print(self.name, self.element, self.abilities, self.health)

    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value):
        self._health=min(self.max_health, max(0, value))

class Player(pygame.sprite.Sprite, Attributes):
    def __init__(self, name, surf):
        super().__init__()
        self.image=surf
        self.rect=self.image.get_rect(bottomleft = (200, window_height))
        self.get_data(name)

    def __repr__(self):
        return f'{self.name}:{self.health}/{self.max_health}'

class Enemy(pygame.sprite.Sprite, Attributes):
    def __init__(self, name, surf, groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(midbottom = (window_width-450, 400))

        self.get_data(name)
        