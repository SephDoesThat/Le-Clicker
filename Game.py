import pygame, sys, json, random
from pygame.locals import *
import os.path
from os import path

#Our py file imports
import global_variables as gvs
import settings as s

import player_classes as pcl
import enemy_classes as ecl
import classless_definitions as funk

pygame.init()

#Save game variable containing mana and unit counts ***
G_Var = [gvs.mana, pcl.P_Var, ecl.E_Var]

#Timer controling "per second events" updating per millisecond
Evoke = pygame.USEREVENT + 1
pygame.time.set_timer(Evoke, 1)
#Enemy spawn timer
Spawn = pygame.USEREVENT + 2
pygame.time.set_timer (Spawn, random.randint(3000, 8000))


#Button super class *** figure out moving pcl and ecl variables here and inheriting
class Button(pygame.sprite.Sprite):
    def __init__(self, size, pos, color, mcolor, ccolor, value):
        super().__init__()
        self.surf = pygame.Surface (size)
        self.rect = self.surf.get_rect(center = (pos))
        self.color = color
        self.mcolor = mcolor
        self.ccolor = ccolor
        self.cost = value
        
    #Function to change color on mouseover and click
    def button_color(self):
        if self.rect.collidepoint(gvs.mouse) == False:
            self.surf.fill(self.color)
        elif self.rect.collidepoint(gvs.mouse):
            if gvs.click == False:
                self.surf.fill(self.mcolor)
            if gvs.click == True:
                self.surf.fill(self.ccolor)



#Buttons for units and eventually other stuff too        
Mana_Button = Button((80, 80), (70, 100), s.BLUE, s.L_BLUE, s. D_BLUE, 0)
Apprentice_Button = Button((80, 40), (s.width -70, 70), s.GRAY, s.L_GRAY, s. D_GRAY, 10)
Mage_Button = Button((80, 40), (s.width -70, 140), s.GRAY, s.L_GRAY, s. D_GRAY, 100)

gvs.all_buttons.add(Mana_Button)
gvs.all_buttons.add(Apprentice_Button, Mage_Button)

#Function updating purchase costs in real time
def update_cost():
    Apprentice_Button.cost = 10+int(pcl.P_Var.get('Apprentices'))
    Mage_Button.cost = 100+int(pcl.P_Var.get('Mages')*15)

#Load game control variable
Loaded = False
#Save function execued on exit currently
def save():
    G_Var[0] = gvs.mana
    with open("Save_Game.json", "w") as savegame:
        json.dump(G_Var, savegame)
        pygame.quit()
        sys.exit()


#Game Loop
while True:
    #Load game
    if Loaded == False:
        if path.exists("Save_Game.json"):
            loadgame = open('Save_Game.json')
            G_Var = json.load(loadgame)
            gvs.mana = G_Var[0]
            pcl.P_Var = G_Var[1]
            ecl.E_Var = G_Var[2]

            for _ in range(pcl.P_Var['Apprentices']):
                Ap_1 = pcl.Apprentice(.001)
                gvs.apprentices.add(Ap_1)

            for _ in range(pcl.P_Var['Mages']):
                Mg_1 = pcl.Mage(.012)
                gvs.mages.add(Mg_1)
                
                 
            for _ in range(ecl.E_Var['Manasquitos']):
                Ms_1 = ecl.Manasquito(.02, 10, s.RED, s.L_RED, s.D_RED)
                gvs.enemies.add(Ms_1)
                gvs.all_buttons.add(Ms_1)
                
            for _ in range(ecl.E_Var['Suckyoubus']):
                Suck_1 = ecl.Suckyoubus(.02, 10, s.RED, s.L_RED, s.D_RED)
                gvs.enemies.add(Suck_1)
                gvs.all_buttons.add(Suck_1)
                

            update_cost()

            Loaded = True

    #Event loop
    for event in pygame.event.get():
        #Exit condition
        if event.type == QUIT:
            save()
            pygame.quit()
            sys.exit()

        #"Per second" timer effects
        if event.type == Evoke:
            for each in gvs.apprentices:
                each.Evoke()
            for each in gvs.mages:
                each.Evoke()
            for each in gvs.enemies:
                each.Unvoke()

        #Enemy spawn events
        if event.type == Spawn:
            ecl.spawn_roll = random.randint(0, gvs.playerlevel)
            ecl.spawn_enemy()
            
        #Click based events
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Manual (click based) mana generation
            if Mana_Button.rect.collidepoint(gvs.mouse):
                if gvs.click == False:
                    gvs.mana += 1
                    gvs.click = True
            #Unit purchasing
            if Apprentice_Button.rect.collidepoint(gvs.mouse) and gvs.mana >= Apprentice_Button.cost:
                if gvs.click == False:
                    gvs.mana -= Apprentice_Button.cost
                    pcl.P_Var['Apprentices'] += 1
                    Ap_1 = pcl.Apprentice(.001)
                    gvs.apprentices.add(Ap_1)
                    gvs.click = True
            if Mage_Button.rect.collidepoint(gvs.mouse) and gvs.mana >= Mage_Button.cost:
                if gvs.click == False:
                    gvs.mana -= Mage_Button.cost
                    pcl.P_Var['Mages'] += 1
                    Mg_1 = pcl.Mage(.012)
                    gvs.mages.add(Mg_1)
                    gvs.click = True
            #Enemy combat (clicking on enemies to murder them)
            for each in gvs.enemies:
                if each.rect.collidepoint(gvs.mouse):
                    each.health -= 1
                    if each.health == 0:
                        ecl.kill_enemy(each)
                        
        #Release control for mouse to prevent repeated triggering on mouse button hold
        if event.type == pygame.MOUSEBUTTONUP:
            gvs.click = False

    #Mouse position detection
    gvs.mouse = pygame.mouse.get_pos()


    #Screen background/fill
    s.screen.fill(s.WHITE)

    #Button rendering
    for each in gvs.all_buttons:
        s.screen.blit(each.surf, each.rect)
        each.button_color()

    #Numerical dispaly for 
    apprentice_display = s.font.render(str(pcl.P_Var['Apprentices']), True, s.L_GRAY)
    s.screen.blit(apprentice_display, (s.width-200, 50))
    mage_display = s.font.render(str(pcl.P_Var['Mages']), True, s.L_GRAY)
    s.screen.blit(mage_display, (s.width-200, 120))

    #Text display for mana
    mana_display = s.font.render(str(int(gvs.mana)), True, s.L_BLUE)
    s.screen.blit(mana_display, (30, 10))
    #Text display for mana per second minus mana drain with total
    mps = (int(pcl.P_Var['Apprentices']))+(int(pcl.P_Var['Mages'])*12)
    mpsx = (ecl.E_Var['Manasquitos'])+(ecl.E_Var['Suckyoubus']*25)
    mps_display = s.tiny_font.render(str('MpS: '+str(mps)+ ' - '+str(mpsx)+ ' = '+str(mps-mpsx)), True, s.L_BLUE)
    s.screen.blit(mps_display, (120, 55))


    #Player level calculation to control and inhibit game events
    gvs.playerlevel = (int(pcl.P_Var['Apprentices']))+(int(pcl.P_Var['Mages'])*12)

    update_cost()
    pygame.display.update()

    
