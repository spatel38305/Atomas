#!/usr/bin/env python3
from StateMachine import *
from Renderer import *

def InitializeGame( args ):
    stateMachine = StateMachine( 18 )
    
    if args and 'render' in args and args['render'] == True:
        return (stateMachine, Renderer())
    else:        
        return (stateMachine, None)

def AtomasGameLoop( stateMachine, renderer ):
    iteration = 0

    running = True
    while( running ):
        
        mctx = stateMachine.MachineContext()
        smi = None

        if renderer:
            renderer.updateStateMachine(mctx)
            renderer.drawFrame()
            renderer.getInput()
            if renderer.running == False:
                running = False
                break

            smi = renderer.getStateMachineInput()
            
        else:
            #TODO automate input
            # smi = ai.getStateMachineInput()
            pass

        stateMachine.input(smi)

        iteration += 1

def main():
    args = {'render': True}

    stateMachine, renderer = InitializeGame( args )
    AtomasGameLoop( stateMachine, renderer )

if __name__ == "__main__":
    main()