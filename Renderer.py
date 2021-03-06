#!/usr/bin/env python3
import pygame
import math

import Game
import utils

#global data representing the atom visuals
ptableSymbols = ['H', 'He', 'Li', 'Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Uub','___','Uuq']
ptable = {i: {'symbol': s, 'color': utils.toColor(i)} for (i,s) in enumerate(ptableSymbols)}
ptable['+'] = {'symbol': '+', 'color': (200,0,0)}
ptable['-'] = {'symbol': '-', 'color': (200,200,200)}

class Renderer():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1920/2,1080/2))
        self.clock = pygame.time.Clock()
        x, y = self.screen.get_size()
        self.x = x
        self.y = y
        self.fps = 60
        self.center = (x/2, y/2)
        self.entities = []
        self.radius = min(x,y)/3
        self.atomRadius = self.radius/6
        self.fontSize = int(self.atomRadius/2)
        self.font = pygame.font.SysFont('roboto', self.fontSize)
        self.offset = -math.pi/2
        self.backgroundColor = (255, 255, 255)
        self.last_mctx = None
        self.mctx = None
        self.stateMachineUpdates = []
        self.createWorld()

    def draw(self, entity):
        '''
        runs pygame's corresponding functions to draw entity args
        '''
        for cmd in entity:
            cmd['fn'](*cmd['args'])

    def createAtomEntity(self, atom, x, y):
        '''
        creates an Atom of rank atom with an x and y position
        '''
        if atom._Value == '+' or atom._Value == '-':
            txt = self.font.render(atom._Value, True, (255,255,255))
            return [
                {'fn': pygame.draw.circle, 'args': [self.screen, ptable[atom._Value]['color'], [x,y], self.atomRadius] },
                {'fn': self.screen.blit, 'args': [txt, (x-self.fontSize/2,y-self.fontSize/2 - self.atomRadius/5)]}
            ]
        else:
            txt = self.font.render(ptable[atom._Value]['symbol'], True, (255,255,255))
            number = self.font.render(str(atom._Value + 1), True, (255,255,255))
            return [
                    {'fn': pygame.draw.circle, 'args': [self.screen, ptable[atom._Value]['color'], [x,y], self.atomRadius] },
                    {'fn': self.screen.blit, 'args': [txt, (x-self.fontSize/2,y-self.fontSize/2 - 1.5*self.atomRadius/5)]},
                    {'fn': self.screen.blit, 'args': [number, (x-self.fontSize/2,y-self.fontSize/2 + self.atomRadius/5)]}
                ]

    def createAtomCircleEntity(self, atom, rad):
        '''
        creates an Atom of rank atom on the circle at a position based on rad (in radians)
        '''
        x = self.radius*math.cos(rad) + self.center[0]
        y = self.radius*math.sin(rad) + self.center[1]
        return self.createAtomEntity(atom, x, y)

    def createAtomCircleEntities(self, atoms):
        '''
        create all atoms in the circle based off of the mctx
        '''
        entities = []
        for i, a in enumerate(atoms):
            entities += self.createAtomCircleEntity(a, (2*math.pi)*(i/len(atoms)) + self.offset)
        return entities

    def drawFrames(self):
        '''
        draws (and animates) all frames. 
        '''
        #self.offset += 0.005
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return [{'GameOver': []}]
                
        self.screen.fill(self.backgroundColor)
        if(len(self.mctx._MergedAtoms) > 0):
            self.animateMerge()
        dynamicEntities = self.createAtomCircleEntities(self.mctx._AtomCircle)
        dynamicEntities += self.createAtomEntity(self.mctx._CenterAtom, self.center[0], self.center[1])

        self.draw(self.entities + dynamicEntities)
        pygame.display.flip()
        self.clock.tick(self.fps)
        return []

    def createWorld(self):
        '''
        draws the environment, a big hollow circle in the center of the screen
        '''
        x, y = self.screen.get_size()
        self.entities.append({'fn': pygame.draw.circle, 'args': [self.screen, (200,200,200), [x/2, y/2], self.radius+self.atomRadius+5+1]})
        self.entities.append({'fn': pygame.draw.circle, 'args': [self.screen, self.backgroundColor, [x/2, y/2], self.radius+self.atomRadius+5-1]})

    def animateNewAtom(self, idx):
        '''
        animates a new atom being thrown, moving the atom circle around
        '''
        frames = int(self.fps/3)
        n = len(self.mctx._AtomCircle)

        rad = ((2*math.pi*idx)/(n+1) + self.offset) % (2*math.pi) if n != 0 else -math.pi/2
        d = (idx/(n*(n+1)) - 1/(n+1))*2*math.pi if n != 0 else 0

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

    def animateMerge(self):
        return

    def handleClick(self, event):
        '''
        handles user input events
        '''
        if self.mctx._Convertable:
            x1 = self.center[0]
            y1 = self.center[1]
            x2, y2 = event.pos
            d = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if d <= self.atomRadius:
                self.stateMachineUpdates.append({'convertAtom': []})
                return

        x, y = self.center
        dx = event.pos[0] - x
        dy = event.pos[1] - y
        rad = math.atan2(dy, dx)
        rad = (rad - self.offset) % (2*math.pi)
        idx = math.ceil(rad/(2*math.pi)*len(self.mctx._AtomCircle))

        self.animateNewAtom(idx)
        self.stateMachineUpdates.append({'addAtom': [self.mctx._CenterAtom._Value, idx]})

    def handleCapture(self, event):
        '''
        handles when user clicks on absorbing an atom when minus atom is the center atom
        '''
        clickedAtomIdx = -1
        ln = len(self.mctx._AtomCircle)
        for i in range(ln):
            rad = (2*math.pi)*(i/ln) + self.offset
            x1 = self.radius*math.cos(rad) + self.center[0]
            y1 = self.radius*math.sin(rad) + self.center[1]
            x2, y2 = event.pos
            d = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if d <= self.atomRadius:
                clickedAtomIdx = i
                break
        
        if clickedAtomIdx != -1:
            self.stateMachineUpdates.append({'minusAtom': [clickedAtomIdx]})
        return clickedAtomIdx

    def getInput(self):
        '''
        gets the raw inputs from pygame.event.get() and passes it on to handleCapture or handleInput depending on the state of the game
        also handles quitting or invalid buttons
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateMachineUpdates.append({'GameOver': []})
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    return
                if self.mctx._CenterAtom._Value == '-':
                    self.handleCapture(event)
                else:
                    self.handleClick(event)
        return self.getStateMachineInput()

    def updateStateMachine(self, mctx):
        '''
        update the internal representation of the state machine
        '''
        self.stateMachineUpdates = []
        self.last_mctx = self.mctx
        self.mctx = mctx

    def getStateMachineInput(self):
        '''
        return the updated statemachine that we modify when user interacts with their inputs
        '''
        return self.stateMachineUpdates