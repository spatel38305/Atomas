#!/usr/bin/env python3
from StateMachine import *
from Renderer import *
from cli import *
import argparse

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
        '''
        entering input into the game (via smi)
        runs a single tick of the game.
        This includes checking if the game is over,
        (optionally) running debug commands,
        (optionally) rendering the game to the screen,
        returning the game's new statemachine context (via mctx)
        '''
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
    '''
    driver code for running main
    '''
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

def cli():
    '''
    cli function responsible for parsing command line arguments.
    -render: if the game should render output (set to false for when running bots)
    -interactive: if the user should have the ability to interact with the rendering
    -debug: if the debug daemon should start, listening for debug commands
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-render', dest='render', type=bool, default=True)
    parser.add_argument('-interactive', dest='interactive', type=bool, default=True)
    parser.add_argument('-debug', dest='debug', type=bool, default=False)
    args = parser.parse_args()
    main(vars(args))
    
if __name__ == "__main__":
    cli()