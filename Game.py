#!/usr/bin/env python3
from threading import Thread

from StateMachine import *
from Renderer import *
from ContextConverter import *
from cli import docli

cli = ''
def get_user_cli_input():
    global cli
    print('waiting debug input...')
    while True:
        cli = input()

def InitializeGame( args ):
    stateMachine = StateMachine( 18 )
    if args == None:
        return (stateMachine, Renderer(), True, ContextConverter())
    else:
        bot = True if 'bot' in args and args['bot'] == True else False
        render = Renderer() if 'render' in args and args['render'] == True else False
        debug = True if 'debug' in args and args['debug'] == True else False
        
        if debug:
            t = Thread(target=get_user_cli_input)
            t.daemon = True
            t.start()

        if bot == False and render == False:
            raise Exception('Render off and Bot off, one must be on!')
        return (stateMachine, Renderer(), bot, ContextConverter(), debug)

def AtomasGameLoop( stateMachine, renderer, bot, contextConverter, debug):
    global cli
    iteration = 0

    while( True ):
        mctx = stateMachine.MachineContext()
        smi = []

        if mctx._Running == False:
            break
        

        if renderer:
            renderer.updateStateMachine(mctx)
            smi += renderer.drawFrames()
            if not bot:
                renderer.getInput()
                smi += renderer.getStateMachineInput()

        elif bot:
            contextConverter.updateContext( mctx )
            contextConverter.convertContext()
            convertedMctx = contextConverter.getConvertedContext()
            print( convertedMctx )
            # smi = ai.getStateMachineInput( convertedMctx )
            smi += {}
            #TODO make sure center atom is convertable for convert action.

        if debug:
            smi += docli(cli)
            cli = ''

        stateMachine.input(smi)

        iteration += 1

def main():    
    args = {'render': True, 'bot': False, 'debug': True}

    try:
        AtomasGameLoop( *InitializeGame( args ) )
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    main()
