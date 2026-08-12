# settings.py

import pygame
import os
from os import walk
from os.path import join
import random
from random import choice
print('starting')
print('pygame imported')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Working directory:", os.getcwd())
(os.path.abspath(__file__))

window_width, window_height = 1200, 720
raw_tile_size = 16 # actual tile size
tile_size = 64 # tile size appearing on screen
player_scale = 3
scale = 4
interaction_range = 512

# colors
pink = (255, 182, 193)
black = (0, 0, 0)
green = (0, 200, 0)
dark_green = (0, 150, 0)
red = (255, 0, 0)
dark_red = (200, 0, 0)
dark_blue = (39,39,87)
white = (255, 255, 255)

# battle colours
colours={
    'black':'#000000',
    'red':'#ee1a0f',
    'gray':'gray',
    'white':'#ffffff',
    'pink':'#f7879a',
    }

enemy_data={
    'Slime':{'element':'water', 'health':80},
    'aurelia':{'element':'plant', 'health':100},
    'kai':{'element':'fire', 'health':100},
    'qiqi':{'element':'plant', 'health':100},
    }

abilities_data={
    'scratch':{'damage':20, 'element':'normal', 'animation':'scratch'},
    'spark':{'damage':30, 'element':'fire', 'animation':'fire'},
    'nuke':{'damage':50, 'element':'fire', 'animation':'explosion'},
    'splash':{'damage':30, 'element':'water', 'animation':'splash'},
    'shards':{'damage':50, 'element':'ice', 'animation':'ice'},
    'spiral':{'damage':40, 'element':'plant', 'animation':'green'},
    }

element_data={
    'fire':    {'water':0.5, 'ice':1, 'plant':2, 'fire':1, 'normal':1.2, 'special':0.5},
    'water':   {'water':0.5, 'ice':1, 'plant':0.5, 'fire':2, 'normal':1, 'special':0.5},
    'ice':     {'water':2, 'ice':1, 'plant':1, 'fire':1, 'normal':1, 'special':0.5},
    'plant':   {'water':2, 'ice':1, 'plant':1, 'fire':0.5, 'normal':1, 'special':0.5},

    'normal':  {'water':1, 'ice':1, 'plant':1, 'fire':1, 'normal':1, 'special':0.5},
    # can add more :), but must add them to each element data as it would otherwise cause a key error
    'special': {'water':3, 'ice':1, 'plant':3, 'fire':3, 'normal':3, 'special':1},

    }