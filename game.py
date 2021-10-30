#!/usr/bin/env python3
from Atomas import *
from Renderer import *

def InitializeGame( args ):
    game = Game( 18 )
    
    if args and 'render' in args and args['render'] == True:
        return (game, Renderer())
    else:        
        return (game, None)

def AtomasGameLoop( game, renderer ):
    iteration = 0

    atom = game.GenerateAtom()
    for i in range(5):
        game.addAtom( atom, 0 )

    running = True
    while( running ):
        
        ctx = game.MachineContext()
        if renderer:
            renderer.drawFrame(ctx)
            renderer.getInput(ctx)
            if renderer.running == False:
                running = False
        else:
            #TODO automate input
            pass

        iteration += 1

def main():
    args = {'render': True}

    game, renderer = InitializeGame( args )
    AtomasGameLoop( game, renderer )

if __name__ == "__main__":
    main()