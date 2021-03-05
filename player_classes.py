import pygame, sys
import global_variables as gvs

pygame.init()

#Stores unit counts
P_Var = {'Apprentices': 0, 'Mages': 0}

#Mana generation units
class Mana_Gen(pygame.sprite.Sprite):
    def __init__(self, pot):
        super().__init__()
        self.potency = pot

    def Evoke(self):
        gvs.mana += self.potency

#Apprentice Class
class Apprentice(Mana_Gen):
    def __init__(self, pot):
        super().__init__(pot)
        self.lure = 1

#Mage Class
class Mage(Mana_Gen):
    def __init__(self, pot):
        super().__init__(pot)
        self.lure = 12
