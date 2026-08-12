import pygame
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from dialogue import dialogue

class Game:
    def __init__(self):
        # setup
        pygame.init()

        self.screen = pygame.display.set_mode((window_width,window_height))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('../data/fonts/PixelOperator.ttf', 32)
        self.was_near_npc = False

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.npc_sprites= pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # dialogue
        self.dialogue_active = False
        self.current_npc = None
        self.current_line_index = 0
        self.nearby_npc = None
        self.battle_triggered = False
        self.triggered_enemy = None

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
            print(f"Entity found: '{marker.name}'")
            if marker.name == 'Player':
                self.player = Player((marker.x*scale, marker.y*scale), self.all_sprites, self.collision_sprites)
            elif marker.name == 'Aurelia':
                NPC((marker.x*scale, marker.y*scale), pygame.transform.scale_by(pygame.image.load('../images/aurelia/L0.png').convert_alpha(), player_scale), (self.all_sprites, self.npc_sprites), marker.name)
            elif marker.name in enemy_data:
                OverworldEnemy((marker.x*scale, marker.y*scale), pygame.transform.scale_by(pygame.image.load('../images/enemies/no_image_enemy.png').convert_alpha(), player_scale), (self.all_sprites, self.enemy_sprites), marker.name)

    def check_npc_proximity(self):
        self.nearby_npc = None
        for npc in self.npc_sprites:
            if self.player.hitbox_rect.inflate(interaction_range, interaction_range).colliderect(npc.rect):
                self.nearby_npc = npc
                break
        is_near_now = self.nearby_npc is not None

        #only triggers if the player has moved from not near to near an NPC
        if is_near_now and not self.was_near_npc and not self.dialogue_active:
            self.dialogue_active = True
            self.current_npc = npc
            self.current_line_index = 0
        self.was_near_npc = is_near_now

    def check_enemy_proximity(self):
        for enemy in self.enemy_sprites:
            print(f"Checking enemy: {enemy.name}, player pos: {self.player.hitbox_rect.center}, enemy pos: {enemy.rect.center}")
            if self.player.hitbox_rect.inflate(interaction_range, interaction_range).colliderect(enemy.rect):
                print("Collision detected!")
                if not self.battle_triggered:
                    self.battle_triggered = True
                    self.triggered_enemy = enemy

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if not self.dialogue_active:
                self.check_npc_proximity()
            if not self.dialogue_active and not self.battle_triggered:
                self.check_npc_proximity()
                self.check_enemy_proximity()
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.dialogue_active:
                        lines = dialogue[self.current_npc.name]
                        if self.current_line_index + 1 < len(lines):
                            self.current_line_index += 1
                        else:
                            self.dialogue_active = False
                            self.current_npc = None
                            self.current_line_index = 0
            # update
            self.all_sprites.update(dt, can_move=not self.dialogue_active)
            for sprite in self.all_sprites:
                if sprite is not self.player:
                    sprite.update(dt)

            #draw
            self.all_sprites.draw(self.player.rect.center)
            for sprite in self.collision_sprites:
                pygame.draw.rect(
                    self.screen,
                    "red",
                    sprite.rect.move(self.all_sprites.offset),
                    2
                )
            if self.dialogue_active:
                box_rect = pygame.Rect(50, window_height - 150, window_width - 100, 100)
                pygame.draw.rect(self.screen, "black", box_rect)
                pygame.draw.rect(self.screen, "white", box_rect, 2)

                text = dialogue[self.current_npc.name][self.current_line_index]
                text_surf = self.font.render(text, True, "white")
                self.screen.blit(text_surf, (box_rect.x + 20, box_rect.y + 20))


            pygame.display.update()

        pygame.quit()  # only after the loop ends
        
if __name__ == '__main__':
    game = Game()
    game.run()
