import pygame, sys
from pygame.locals import*

pygame.init()

#Display settings
res = (720, 720)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()

fps = 60

#Fonts
font = pygame.font.SysFont("Corbel", 40)
tiny_font = pygame.font.SysFont("Corbel", 20)

#Default colors
WHITE = (255, 255, 255)
L_GRAY = (160, 160, 160)
GRAY = (130, 130, 130)
D_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

L_BLUE = (170, 170, 255)
BLUE = (20, 20, 140)
D_BLUE = (20, 20, 60)

L_RED =(255, 170, 170)
RED = (140, 20, 20)
D_RED = (100, 20, 20)
