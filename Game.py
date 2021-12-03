#!/usr/bin/env python3
from StateMachine import *
from Renderer import *
from cli import *

class Game:
    def __init__(self, render=False, interactive=True, debug=False):
        self.stateMachine = StateMachine( 18 )
        self.iteration = 0
        self.renderer = Renderer() if render else False
        self.interactive = interactive
        self.debug = debug
        if self.debug:
            startcli(self)

    def runTick(self, smi):
        mctx = self.stateMachine.input(smi)

        if mctx._Running == False:
            return mctx

        if self.debug:
            dbg = docli(self.cli)
            self.stateMachine.input(dbg)
            self.cli = ''

        if self.renderer:
            self.renderer.updateStateMachine(mctx)
            smi += self.renderer.drawFrames()

        self.iteration += 1
        return mctx


def main(args={}):
    game = Game(**args)
    smi = []
    running = True
    while running:
        mctx = game.runTick(smi)
        running = mctx._Running
        smi = []
        if game.renderer and game.interactive:
            smi += game.renderer.getInput()
    print('Game Over')
    print(mctx._CurrentScore)

if __name__ == "__main__":
    args = {'render': True, 'interactive': True, 'debug': True}
    main(args)
