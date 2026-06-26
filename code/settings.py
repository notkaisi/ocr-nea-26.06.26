import pygame
import os
from os import walk
import random
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

# colors
pink = (255, 182, 193)
black = (0, 0, 0)
green = (0, 200, 0)
dark_green = (0, 150, 0)
red = (255, 0, 0)
dark_red = (200, 0, 0)
dark_blue = (39,39,87)
white = (255, 255, 255)

