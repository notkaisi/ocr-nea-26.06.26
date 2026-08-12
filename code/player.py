#player

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # lists of images for each direction
        self.images = {
            'up': [pygame.transform.scale_by(pygame.image.load(f'../images/mizu/U{i}.png').convert_alpha(), player_scale) for i in range(3)],
            'down': [pygame.transform.scale_by(pygame.image.load(f'../images/mizu/D{i}.png').convert_alpha(), player_scale) for i in range(3)],
            'left': [pygame.transform.scale_by(pygame.image.load(f'../images/mizu/L{i}.png').convert_alpha(), player_scale) for i in range(3)],
            'right': [pygame.transform.scale_by(pygame.image.load(f'../images/mizu/R{i}.png').convert_alpha(), player_scale) for i in range(3)],
        }

        self.direction_facing = 'down'
        self.frame_index = 0
        self.image = self.images[self.direction_facing][self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-10, -70) 

        # animation timer
        self.animation_timer = 0
        self.animation_speed = 0.15  # seconds per frame, lower = faster

        #movement
        self.direction = pygame.Vector2()
        self.speed = 250
        self.collision_sprites = collision_sprites

        #animation
    def animate(self, dt):
        if self.direction.length() > 0:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.images[self.direction_facing])
        else:
            self.frame_index = 0
        self.image = self.images[self.direction_facing][self.frame_index]

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

            if self.direction.x > 0: self.direction_facing = 'right'
            elif self.direction.x < 0: self.direction_facing = 'left'
            elif self.direction.y < 0: self.direction_facing = 'up'
            elif self.direction.y > 0: self.direction_facing = 'down'

    def move(self, dt): 
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.hitbox_rect):
                        if direction == 'horizontal':
                            if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                            if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                        else:
                            if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                            if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def update(self, dt, can_move=True):
        if can_move:
            self.input()
            self.move(dt)
        else:
            self.direction = pygame.Vector2()
        self.animate(dt)