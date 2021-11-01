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
        pygame.font.init()
        self.fontSize = 10
        self.font = pygame.font.SysFont('roboto', self.fontSize)
        self.screen = pygame.display.set_mode((1920/4,1080/4))
        self.clock = pygame.time.Clock()
        x, y = self.screen.get_size()
        self.x = x
        self.y = y
        self.fps = 30
        self.center = (x/2, y/2)
        self.entities = []
        self.running = True
        self.radius = min(x,y)/3
        self.atomRadius = self.radius/6
        self.offset = -math.pi/2
        self.backgroundColor = (255, 255, 255)
        self.mctx = None
        self.stateMachineUpdates = []
        self.createWorld()

    def draw(self, entity):
        for cmd in entity:
            cmd['fn'](*cmd['args'])

    def createAtomEntity(self, atom, x, y):
        txt = self.font.render(ptable[atom._Value]['symbol'], True, (255,255,255))
        number = self.font.render(str(atom._Value), True, (255,255,255))
        return [
                {'fn': pygame.draw.circle, 'args': [self.screen, ptable[atom._Value]['color'], [x,y], self.atomRadius] },
                {'fn': self.screen.blit, 'args': [txt, (x-self.fontSize/2,y-self.fontSize/2 - 3)]},
                {'fn': self.screen.blit, 'args': [number, (x-self.fontSize/2,y-self.fontSize/2 + 5)]}
            ]

    def createAtomCircleEntity(self, atom, rad):
        x = self.radius*math.cos(rad) + self.center[0]
        y = self.radius*math.sin(rad) + self.center[1]
        return self.createAtomEntity(atom, x, y)

    def createAtomCircleEntities(self, atoms):
        entities = []
        for i, a in enumerate(atoms):
            entities += self.createAtomCircleEntity(a, (2*math.pi)*(i/len(atoms)) + self.offset)
        return entities

    def drawFrame(self):
        #self.offset += 0.005
        self.screen.fill(self.backgroundColor)
        dynamicEntities = self.createAtomCircleEntities(self.mctx._AtomCircle)
        dynamicEntities += self.createAtomEntity(self.mctx._CenterAtom, self.center[0], self.center[1])

        self.draw(self.entities + dynamicEntities)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def createWorld(self):
        x, y = self.screen.get_size()
        self.entities.append({'fn': pygame.draw.circle, 'args': [self.screen, (200,200,200), [x/2, y/2], self.radius+self.atomRadius+5+1]})
        self.entities.append({'fn': pygame.draw.circle, 'args': [self.screen, self.backgroundColor, [x/2, y/2], self.radius+self.atomRadius+5-1]})

    def animateNewAtom(self, idx):
        frames = 10
        n = len(self.mctx._AtomCircle)
        rad = ((2*math.pi*idx)/n - 7*math.pi/(4*n) + self.offset) % (2*math.pi)
        
        d = (idx/(n*(n+1)) - 1/(n+1))*2*math.pi
        rad -= d

        for f in range(frames):
            self.offset -= d/frames
            self.screen.fill(self.backgroundColor)
            dynamicEntities = []
            
            for cidx in range(n):
                i = (idx + cidx) % n
                r = cidx/(n + (f/frames)) + idx/n

                crad = (r*2*math.pi + self.offset) % (2*math.pi)
                dynamicEntities += self.createAtomCircleEntity(self.mctx._AtomCircle[i], crad)


            x = (f/frames)*self.radius*math.cos(rad) + self.center[0]
            y = (f/frames)*self.radius*math.sin(rad) + self.center[1]
            dynamicEntities += self.createAtomEntity(self.mctx._CenterAtom, x, y)

            self.draw(self.entities + dynamicEntities)
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        self.offset += d

        for e in pygame.event.get(): #ignore input during this time
            continue



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

        self.animateNewAtom(idx)
        self.stateMachineUpdates.append({'addAtom': [self.mctx._CenterAtom, idx]})

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