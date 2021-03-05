import pygame, sys

pygame.init()

#Click control variable used to stop repeat clicking while holding mouse button
click = False
#Mouse position variable
mouse = pygame.mouse.get_pos()

#Advancement variable used for controlling and pacing content
playerlevel = 0

#Basic resources
mana = 0.0
gold = 0.01

#All sprite groups
all_buttons = pygame.sprite.Group()
apprentices = pygame.sprite.Group()
mages = pygame.sprite.Group()
enemies = pygame.sprite.Group()

