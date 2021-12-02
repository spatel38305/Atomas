#!/usr/bin/env python3
from StateMachine import *
from Renderer import *
from cli import *
import bot

class Game:
    def __init__(self, render=False, interactive=True, bot=True, debug=False):
        self.stateMachine = StateMachine( 18 )
        self.iteration = 0
        self.bot = bot
        self.renderer = Renderer() if render else False
        self.interactive = interactive
        self.debug = debug
        if self.debug:
            startcli(self)
        if self.bot == False and self.renderer == False:
            raise Exception('Render off and Bot off, one must be on!')

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
    if args['bot'] and args['bot'] == True:
        bot.run()
    else:
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
    args = {'render': True, 'interactive': True, 'bot': False, 'debug': True}
    main(args)
