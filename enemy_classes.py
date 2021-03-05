import pygame, sys, random
import settings as s
import global_variables as gvs

pygame.init()

#Stores unit counts
E_Var = {'Manasquitos': 0, 'Suckyoubus': 0}

#Variables controlling enemy spawn
spawn_roll = 0
mosqspawn = 0
suckspawn = 10

#Enemy super class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, epot, hp, color, mcolor, ccolor):
        super().__init__()
        self.epotency = epot
        self.health = hp
        self.color = color
        self.mcolor = mcolor
        self.ccolor = ccolor
        
    #Mana drain function
    def Unvoke(self):  
        if gvs.mana > 0:
            gvs.mana -= self.epotency
        else:
            gvs.mana = 0

    #Function to change color on mouseover and click
    def button_color(self):
        if self.rect.collidepoint(gvs.mouse) == False:
            self.surf.fill(self.color)
        elif self.rect.collidepoint(gvs.mouse):
            if gvs.click == False:
                self.surf.fill(self.mcolor)
            if gvs.click == True:
                self.surf.fill(self.ccolor)
            
#Manasquito Class
class Manasquito (Enemy):
    def __init__(self, epot, hp, color, mcolor, ccolor):
        super().__init__(epot, hp, color, mcolor, ccolor)
        self.type = 'Manasquito'
        self.surf = pygame.Surface((40, 40))
        self.rect = self.surf.get_rect(center = (random.randint(160, s.width-290), random.randint(140, s.height-50)))

#Suckyoubus Class
class Suckyoubus (Enemy):
    def __init__(self, epot, hp, color, mcolor, ccolor):
        super().__init__(epot, hp, color, mcolor, ccolor)
        self.type = 'Suckyoubus'
        self.surf = pygame.Surface((60, 100))
        self.surf.fill(s.D_RED)
        self.rect = self.surf.get_rect(center = (random.randint(170, s.width-260), random.randint(150, s.height-80)))

#Enemy spawn fucnction
def spawn_enemy():
        if spawn_roll >= mosqspawn:
            Ms_1 = Manasquito(.001, 4, s.RED, s.L_RED, s.D_RED)
            E_Var['Manasquitos'] += 1
            gvs.enemies.add(Ms_1)
            gvs.all_buttons.add(Ms_1)
            
        if spawn_roll >= suckspawn:
            Suck_1 = Suckyoubus(.025, 10, s.RED, s.L_RED, s.D_RED)
            E_Var['Suckyoubus'] += 1
            gvs.enemies.add(Suck_1)
            gvs.all_buttons.add(Suck_1)

#Enemy death and clean up function
def kill_enemy(self):
    if self.type == 'Manasquito':
        E_Var['Manasquitos'] -= 1
    
    if self.type == 'Suckyoubus':
        E_Var['Suckyoubus'] -= 1

    self.kill()
        
