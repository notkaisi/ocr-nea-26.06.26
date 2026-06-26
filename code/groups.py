# groups.py

from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2(0, 0)
        self.map_width = 0
        self.map_height = 0

    def set_map_size(self, width, height): # setter method
        self.map_width = width
        self.map_height = height

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)

        if self.map_width and self.map_height:
            min_offset_x = -(self.map_width - window_width)
            offset_x = max(min_offset_x, min(0, self.offset.x))

            min_offset_y = -(self.map_height - window_height)
            offset_y = max(min_offset_y, min(0, self.offset.y))

        self.offset.x = offset_x
        self.offset.y = offset_y

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.screen.blit(sprite.image, (round(sprite.rect.x + self.offset.x), round(sprite.rect.y + self.offset.y))) # position of the sprites does not change