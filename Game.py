#!/usr/bin/env python3
from threading import Thread

from StateMachine import *
from Renderer import *
from ContextConverter import *

cli = ''
def get_user_cli_input():
    global cli
    print('waiting debug input...')
    while True:
        cli = input()

def docli(cli, stateMachine):
    updates = []
    if cli[0] == 'add':
        idx = 0
        if len(cli) > 2:
            idx = int(cli[2])
        a = cli[1]
        if a not in ['+']:
            a = int(a)
        updates.append({'addAtom': [Atom(a), idx]})
    elif cli[0] == 'convert':
        updates.append({'convertAtom': []})
    return updates

def InitializeGame( args ):
    stateMachine = StateMachine( 18 )

    if args and 'render' in args and args['render'] == True:
        return (stateMachine, Renderer(), ContextConverter())
    else:
        return (stateMachine, None, ContextConverter())

def AtomasGameLoop( stateMachine, renderer, contextConverter ):
    global cli
    iteration = 0

    running = True
    while( running ):
        mctx = stateMachine.MachineContext()
        smi = None

        if renderer:
            renderer.updateStateMachine(mctx)
            renderer.drawFrames()
            renderer.getInput()
            if renderer.running == False:
                running = False
                break

            smi = renderer.getStateMachineInput()

        else:
            #TODO automate input
            contextConverter.updateContext( mctx )
            contextConverter.convertContext()
            convertedMctx = contextConverter.getConvertedContext()

            print( convertedMctx )
            # smi = ai.getStateMachineInput( convertedMctx )
            smi = []

            #TODO make sure center atom is convertable for convert action.
            pass

        if cli != '':
            smi = docli(cli.split(), stateMachine)
            cli = ''

        stateMachine.input(smi)

        iteration += 1

def main():

    t = Thread(target=get_user_cli_input)
    t.daemon = True
    t.start()
    args = {'render': True}

    stateMachine, renderer, contextConverter = InitializeGame( args )
    AtomasGameLoop( stateMachine, renderer, contextConverter )

if __name__ == "__main__":
    main()
