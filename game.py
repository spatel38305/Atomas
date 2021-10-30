import pygame
import math

import utils

ptableSymbols = ['H', 'He', 'Li', 'Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Uub','___','Uuq']
ptable = {i: {'symbol': s, 'color': utils.toColor(i)} for (i,s) in enumerate(ptableSymbols)}
        

class Renderer():
    def __init__(self, screen):
        self.screen = screen
        x, y = screen.get_size()
        self.x = x
        self.y = y
        self.center = (x/2, y/2)
        self.entities = []
        self.ptable = ptable
        self.createWorld()

    def drawAtom(id, rad):
        p = ptable[id]

    def draw(self, entity):
        for shape in entity:
            fn = getattr(pygame.draw, shape)
            params = entity[shape]
            if isinstance(params, list):
                fn(*entity[shape])
            elif isinstance(params, dict):
                args = []
                if 'args' in params:
                    args = params['pargs']
                    del params['args']
                fn(*args, **params)

    def drawScreen(self):
        for entity in self.entities:
            self.draw(entity)

    def createWorld(self):
        x, y = self.screen.get_size()
        minSize = min(x,y)
        self.entities.append({'circle': [self.screen, (255,255,255), [x/2, y/2], minSize/4]})

    def handleClick(self, event):
        if event.button != 1:
            return
        
        pos = event.pos
        x, y = self.center
        dx = -(pos[0] - x)
        dy = -(pos[1] - y)
        rad = math.atan2(dy, dx)
        if rad < 0:
            rad += 2*math.pi
        
        idx = round(rad/(2*math.pi)*18)



def main():
    pygame.init()
    screen = pygame.display.set_mode((1920/4,1080/4))
    
    R = Renderer(screen)
    
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                R.handleClick(event)

        R.drawScreen()
        pygame.display.flip()

    

if __name__ == "__main__":
    main()