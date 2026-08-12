#--ui.py--
from settings import *
from enemy import *
class UI:
    def __init__(self, player, player_chars, simple_surfs, get_input):
        self.screen=pygame.display.get_surface()
        self.font=pygame.font.Font(None, 30)
        self.left=window_width/2-100
        self.top=window_height/2+50
        self.player=player
        self.simple_surfs=simple_surfs
        self.get_input=get_input

        # control
        self.general_options=['attack', 'skill', 'switch', 'escape']
        self.general_index={'col':0,'row':0}
        self.attack_index={'col':0,'row':0}
        self.state='general'
        self.rows, self.cols = 2,2
        self.visible_chars=4
        self.player_chars=player_chars
        self.available_chars=[player for player in self.player_chars if player != self.player and player.health>0]
        self.switch_index=0

        # input
    def input(self):
        keys=pygame.key.get_just_pressed()

        if self.state=='general':
            self.general_index['row']=(self.general_index['row']+int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP]))%self.rows
            self.general_index['col']=(self.general_index['col']+int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT]))%self.cols
            if keys[pygame.K_SPACE]:
                self.state=self.general_options[self.general_index['col']+self.general_index['row']*2]

        elif self.state=='attack':
            self.attack_index['row']=(self.attack_index['row']+int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP]))%self.rows
            self.attack_index['col']=(self.attack_index['col']+int(keys[pygame.K_RIGHT])-int(keys[pygame.K_LEFT]))%self.cols
            if keys[pygame.K_SPACE]:
                attack=self.player.abilities[self.attack_index['col']+self.attack_index['row']*2]
                self.get_input(self.state, attack)
                self.state='general'

        elif self.state=='switch':
            if self.available_chars:
                self.switch_index=(self.switch_index+int(keys[pygame.K_DOWN])-int(keys[pygame.K_UP]))%len(self.available_chars)

                if keys[pygame.K_SPACE]:
                    self.get_input(self.state, self.available_chars[self.switch_index])
                    self.state='general'
                
        elif self.state=='skill':
            self.get_input('skill')
            self.state='general'

        elif self.state=='escape':
            self.get_input('escape')


        if keys[pygame.K_ESCAPE]:
            self.state='general'
            self.general_index={'col':0,'row':0}
            self.attack_index={'col':0,'row':0}
            self.switch_index=0

    def quad_select(self, index, options):
        # bg
        rect=pygame.Rect(self.left+40,self.top+60,400,200)
        pygame.draw.rect(self.screen, colours['white'],rect,0,4)
        pygame.draw.rect(self.screen, colours['gray'],rect,5,4) # border

        # menu
        for col in range(self.cols):
            for row in range(self.rows):
                x=rect.left+rect.width/(self.cols*2)+(rect.width/self.cols)*col
                y=rect.top+rect.height/(self.rows*2)+(rect.height/self.rows)*row
                i=col+2*row
                colour=colours['black'] if col==index['col'] and row==index['row'] else colours['gray']


                text_surf=self.font.render(options[i], True, colour)
                text_rect=text_surf.get_rect(center=(x,y))
                self.screen.blit(text_surf, text_rect)

    def update(self):
        self.input()
        self.available_chars=[char for char in self.player_chars if char != self.player and char.health>0]

    def switch(self):
        # bg
        rect=pygame.FRect(self.left+40, self.top-140, 400, 400)
        pygame.draw.rect(self.screen, colours['white'],rect,0,4)
        pygame.draw.rect(self.screen, colours['gray'],rect,5,4)

        # menu
        v_offset=0 if self.switch_index < self.visible_chars else -(self.switch_index-self.visible_chars+1)*rect.height/self.visible_chars
        for i in range(len(self.available_chars)):
            x=rect.centerx
            y=rect.top+rect.height/(self.visible_chars*2)+rect.height/self.visible_chars*i+v_offset #splits the menu into 4 rectangles and finds the center
            colour=colours['black'] if i == self.switch_index else colours['gray']
            name=self.available_chars[i].name

            simple_surf=self.simple_surfs[name]
            simple_rect=simple_surf.get_frect(center=(x-100,y))

            text_surf=self.font.render(name, True, colour)
            text_rect=text_surf.get_frect(midleft = (x,y))
            if rect.collidepoint(text_rect.center): 
                self.screen.blit(text_surf, text_rect)
                self.screen.blit(simple_surf, simple_rect)

    def stats(self):
        # bg
        rect = pygame.FRect(self.left, self.top, 250, 80)
        pygame.draw.rect(self.screen, colours['white'],rect,0,4)
        pygame.draw.rect(self.screen, colours['gray'],rect,5,4)
        # data
        name_surf=self.font.render(self.player.name, True, colours['black'])
        name_rect=name_surf.get_frect(topleft=rect.topleft+pygame.Vector2(rect.width*0.05, 12))
        self.screen.blit(name_surf, name_rect)

        # health bar
        health_rect=pygame.FRect(name_rect.left, name_rect.bottom+10, rect.width*0.9, 20)
        pygame.draw.rect(self.screen, colours['gray'], health_rect)
        self.draw_bar(health_rect, self.player.health, self.player.max_health)

    def draw_bar(self, rect, value, max_value):
        ratio=rect.width/max_value
        progress_rect=pygame.FRect(rect.topleft,(value*ratio,rect.height))
        pygame.draw.rect(self.screen, colours['red'], progress_rect)

    def draw(self):
        match self.state:
            case 'general': self.quad_select(self.general_index, self.general_options)
            case 'attack': self.quad_select(self.attack_index, self.player.abilities)
            case 'switch': self.switch()
        if self.state != 'switch':
            self.stats()

class OpponentUI:
    def __init__(self, enemy):
        self.screen=pygame.display.get_surface()
        self.enemy=enemy
        self.font=pygame.font.Font(None, 30)

    def draw(self):
        # bg
        rect=pygame.FRect((0,0), (250,80)).move_to(midleft=(500,self.enemy.rect.centery))
        pygame.draw.rect(self.screen, colours['white'],rect,0,4)
        pygame.draw.rect(self.screen, colours['gray'],rect,5,4)

        name_surf=self.font.render(self.enemy.name, True, colours['black'])
        name_rect=name_surf.get_frect(topleft=rect.topleft+pygame.Vector2(rect.width*0.05, 12))
        self.screen.blit(name_surf, name_rect)

        # health bar
        health_rect=pygame.FRect(name_rect.left, name_rect.bottom+10, rect.width*0.9, 20)
        ratio=health_rect.width/self.enemy.max_health
        progress_rect=pygame.FRect(health_rect.topleft,(self.enemy.health*ratio,health_rect.height))
        pygame.draw.rect(self.screen, colours['gray'], health_rect)
        pygame.draw.rect(self.screen, colours['red'], progress_rect)