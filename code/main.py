import pygame
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # setup
        self.setup()

        # sprites

    def setup(self):

        map = load_pygame('../data/maps/starter.tmx')

        map_width = map.width * tile_size
        map_height = map.height * tile_size
        self.all_sprites.set_map_size(map_width, map_height)

        for x,y, image in map.get_layer_by_name('Ground').tiles():
            image = pygame.transform.scale_by(image, scale)
            Sprite((x*raw_tile_size*scale,y*raw_tile_size*scale), image, self.all_sprites)

        for x,y, image in map.get_layer_by_name('Foreground').tiles():
            image = pygame.transform.scale_by(image, scale)
            Sprite((x*raw_tile_size*scale,y*raw_tile_size*scale), image, self.all_sprites, ground=False)

        for obj in map.get_layer_by_name('Objects'):
            image = pygame.transform.scale_by(obj.image, scale)
            #print(obj.x, obj.y, obj.width, obj.height)
            #print(image.get_size())
            Sprite((round(obj.x*scale), round(obj.y*scale)), image, self.all_sprites, ground=False)

        for obj in map.get_layer_by_name('Collisions'):
            print(f"Collision object: {obj.name}, position: ({obj.x}, {obj.y}), size: ({obj.width}, {obj.height})")
            # rotated rectangles and polygons are not supported by pygame's rect collision detection
            if obj.rotation != 0:
                print(f"Warning: Rotated collision object at {obj.x}, {obj.y}")
            # ignore polygons
            if hasattr(obj, "points") and obj.points:
                print("Polygon collision not supported")
                print(
                        obj.image.get_size(),
                        image.get_size(),
                        obj.x,
                        obj.y
                    )
            Collision_sprite((round(obj.x*scale), round(obj.y*scale)), pygame.Surface((obj.width*scale, obj.height*scale)), self.collision_sprites)

        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x*scale, marker.y*scale), self.all_sprites, self.collision_sprites)
            elif marker.name == 'Aurelia':
                NPC((marker.x*scale, marker.y*scale), pygame.transform.scale_by(pygame.image.load('../images/aurelia/L0.png').convert_alpha(), player_scale), self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        self.running = False

            # update
            self.all_sprites.update(dt)

            #draw
            self.all_sprites.draw(self.player.rect.center)
            for sprite in self.collision_sprites:
                pygame.draw.rect(
                    self.screen,
                    "red",
                    sprite.rect.move(self.all_sprites.offset),
                    2
                )
            pygame.display.update()

        pygame.quit()  # only after the loop ends
        
if __name__ == '__main__':
    game = Game()
    game.run()
