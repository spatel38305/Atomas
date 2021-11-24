#!/usr/bin/env python3
from StateMachine import *
from Renderer import *
from cli import *

class Game:
    def __init__(self, render=False, interactive=True, bot=True, debug=False):
        self.stateMachine = StateMachine( 18 )
        self.iteration = 0
        self.bot = bot
        self.renderer = Renderer() if render else False
        self.interactive = interactive
        self.debug = debug
        self.smi = []
        if self.debug:
            startcli(self)
        if self.bot == False and self.renderer == False:
            raise Exception('Render off and Bot off, one must be on!')

    def runTick(self, smi):
        mctx = self.stateMachine.input(smi)
        
        if mctx._Running == False:
            raise Exception()
        
        if self.debug:
            smi += docli(self.cli)
            self.cli = ''

        if self.renderer:
            self.renderer.updateStateMachine(mctx)
            smi += self.renderer.drawFrames(smi)
        
        self.iteration += 1
        return mctx

def main(args={}):    
    try:
        game = Game(**args)
        smi = []
        while True:
            game.runTick(smi)
            smi = []
            if game.renderer and game.interactive:
                smi += game.renderer.getInput()
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    args = {'render': True, 'interactive': True, 'bot': True, 'debug': False}
    main(args)
