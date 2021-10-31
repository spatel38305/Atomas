#!/usr/bin/env python3
import pygame
import math

import Game
import utils

ptableSymbols = ['H', 'He', 'Li', 'Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Uub','___','Uuq']
ptable = {i: {'symbol': s, 'color': utils.toColor(i)} for (i,s) in enumerate(ptableSymbols)}
ptable['+'] = {'symbol': '+', 'color': (200,0,0)}
ptable['-'] = {'symbol': '-', 'color': (200,200,200)}

class Renderer():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920/4,1080/4))
        self.clock = pygame.time.Clock()
        x, y = self.screen.get_size()
        self.x = x
        self.y = y
        self.center = (x/2, y/2)
        self.entities = []
        self.ptable = ptable
        self.running = True
        self.radius = min(x,y)/3
        self.atomRadius = self.radius/6
        self.offset = -math.pi/2
        self.mctx = None
        self.stateMachineUpdates = []
        self.createWorld()

    def draw(self, entity):
        for shape in entity:
            utils.applyattr(pygame.draw, shape, entity[shape])

    def createAtomEntities(self, atoms):
        def atomToEntity(atom, i, tot):
            a = ptable[atom._Value]
            rad = (2*math.pi)*(i/tot) + self.offset
            x = self.radius*math.cos(rad) + self.center[0]
            y = self.radius*math.sin(rad) + self.center[1]
            return [self.screen, a['color'], [x,y], self.atomRadius]
        return list(map(lambda a: {'circle': atomToEntity(a[1], a[0], len(atoms))}, enumerate(atoms)))

    def drawFrame(self):
        self.offset += 0.005
        self.screen.fill((255,255,255))
        dynamicEntities = self.createAtomEntities(self.mctx._AtomCircle)
        dynamicEntities += [{'circle': [self.screen, ptable[self.mctx._CenterAtom._Value]['color'], [self.center[0], self.center[1]], self.atomRadius]}]

        for entity in self.entities + dynamicEntities:
            self.draw(entity)
        pygame.display.flip()
        self.clock.tick(60)

    def createWorld(self):
        x, y = self.screen.get_size()
        self.entities.append({'circle': [self.screen, (200,200,200), [x/2, y/2], self.radius+1]})
        self.entities.append({'circle': [self.screen, (255,255,255), [x/2, y/2], self.radius-1]})

    def handleClick(self, event):
        if event.button != 1:
            return
        
        pos = event.pos
        x, y = self.center
        dx = pos[0] - x 
        dy = pos[1] - y 
        rad = math.atan2(dy, dx)
        rad = (rad - self.offset) % (2*math.pi)
        idx = math.ceil(rad/(2*math.pi)*len(self.mctx._AtomCircle))
        self.stateMachineUpdates.append({'addAtom': [self.mctx._CenterAtom, idx]})
        return idx

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(event)

    def updateStateMachine(self, mctx):
        self.stateMachineUpdates = []
        self.mctx = mctx

    def getStateMachineInput(self):
        return self.stateMachineUpdates



if __name__ == "__main__":
    Game.main()