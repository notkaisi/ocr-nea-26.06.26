from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, ground=True):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        if ground:
            self.ground = True

class Collision_sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.name = name

class OverworldEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.name = name