import numpy as np

from StateMachine import *

import Game

def convertContext( mctx ):
    x = np.ndarray( ( 20 ) )
    y = np.ndarray( ( 1 ) )

    if ( mctx._Convertable == True ):
        x[0] = 1
    else:
        x[0] = 0

    if ( mctx._CenterAtom._Value == '+' ):
        x[1] = -1
    elif( mctx._CenterAtom._Value == '-' ):
        x[1] = -2
    else:
        x[1] = mctx._CenterAtom._Value

    for i, a in enumerate( mctx._AtomCircle ):
        x[i + 2] = a._Value

    for i in range( 0, mctx._MaxAtoms - len( mctx._AtomCircle ) ):
        x[i + len( mctx._AtomCircle ) + 2] = 0

    y[0] = mctx._CurrentScore

    return x, y

def convertOutput( bOut, mctx ):
    actions = []
    indices = np.argmax( bOut )
    choice = -1

    #Check if there are multiple indices.
    if ( indices.size > 1 ):
        choice = np.random.choice( indices )
    else:
        choice = indices[0]

    #Check for converting center atom to +.
    if ( choice == 18 ):
        actions.append( { "convertAtom" : [] } )
    else:
        #Check for -.
        if ( mctx._CenterAtom._Value == "-" ):
            actions.append( { "minusAtom" : [ choice ] } )
        else:
            actions.append( { "addAtom" : [ mctx._CenterAtom._Value, choice ] } )

        if ( choice >= len( mctx._AtomCircle ) ):
            actions = []

    return actions

if __name__ == "__main__":
    Game.main()
