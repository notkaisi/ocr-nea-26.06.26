# code/battle/battle.py
import pygame
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from settings import *
from battle.support import *
from battle.timer import Timer
from battle.enemy import Player as BattlePlayer, Enemy, Attributes
from battle.ui import UI, OpponentUI
from battle.attack import AttackAnimationSprite
from random import choice

class Battle:
    def __init__(self, enemy_name, screen):
        self.screen = screen
        self.result = None  # None = ongoing, 'win', 'lose', 'escape'
        self.player_active = True

        self.import_assets()
        for sound in self.audio.values():
            sound.set_volume(0.4)
        self.audio['The Forest'].play(-1)

        self.all_sprites = pygame.sprite.Group()

        player_list = ['mizu', 'aurelia', 'kai', 'qiqi']
        self.player_chars = [BattlePlayer(name, self.back_surfs[name]) for name in player_list]
        self.player = self.player_chars[0]
        self.all_sprites.add(self.player)

        self.enemy = Enemy(enemy_name, self.front_surfs[enemy_name], self.all_sprites)

        self.ui = UI(self.player, self.player_chars, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.enemy)

        self.timers = {
            'player end': Timer(2000, func=self.enemy_turn),
            'enemy end': Timer(1000, func=self.player_turn)
        }

    def get_input(self, state, data=None):
        if state == 'attack':
            self.apply_attack(self.enemy, data)
        elif state == 'skill':
            self.player.health += 50
            AttackAnimationSprite(self.player, self.attack_frames['green'], self.all_sprites)
            self.audio['green'].play()
        elif state == 'switch':
            self.player.kill()
            self.player = data
            self.all_sprites.add(self.player)
            self.ui.player = self.player
        elif state == 'escape':
            self.result = 'escape'
            self.audio['The Forest'].stop()
            return  # don't activate timer if escaping
        self.player_active = False
        self.timers['player end'].activate()

    def apply_attack(self, target, attack):
        attack_data = abilities_data[attack]
        attack_multiplier = element_data[attack_data['element']][target.element]
        target.health -= attack_data['damage'] * attack_multiplier
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
        self.audio[attack_data['animation']].play()

    def enemy_turn(self):
        if self.enemy.health <= 0:
            self.result = 'win'
            self.audio['The Forest'].stop()
        else:
            attack = choice(self.enemy.abilities)
            self.apply_attack(self.player, attack)
            self.timers['enemy end'].activate()

    def player_turn(self):
        self.player_active = True
        if self.player.health <= 0:
            available_chars = [p for p in self.player_chars if p.health > 0]
            if available_chars:
                self.player.kill()
                self.player = available_chars[0]
                self.all_sprites.add(self.player)
                self.ui.player = self.player
            else:
                self.result = 'lose'
                self.audio['The Forest'].stop()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.back_surfs = folder_importer('..', 'images', 'back')
        self.front_surfs = folder_importer('..', 'images', 'front')
        self.bg_surfs = folder_importer('..', 'images', 'other')
        self.simple_surfs = folder_importer('..', 'images', 'simple')
        self.attack_frames = tile_importer(4, '..', 'images', 'attacks')
        self.audio = audio_importer('..', 'audio')

    def draw_sprite_shadow(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Attributes):
                shadow_rect = self.bg_surfs['shadow'].get_rect(
                    center=sprite.rect.midbottom + pygame.Vector2(0, -10)
                )
                self.screen.blit(self.bg_surfs['shadow'], shadow_rect)

    def update(self, dt):
        self.update_timers()
        self.all_sprites.update(dt)
        if self.player_active:
            self.ui.update()

    def draw(self):
        self.screen.blit(self.bg_surfs['bg'], (0, 0))
        self.draw_sprite_shadow()
        self.all_sprites.draw(self.screen)
        self.ui.draw()
        self.opponent_ui.draw()