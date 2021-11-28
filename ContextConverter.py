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
        v = -1 if a._Value == '+' else a._Value
        x[i + 2] = v

    for i in range( 0, mctx._MaxAtoms - len( mctx._AtomCircle ) ):
        x[i + len( mctx._AtomCircle ) + 2] = 0

    y[0] = mctx._CurrentScore + mctx._TotalThrown

    return x, y

def convertOutput( bOut, mctx ):
    actions = []
    indices = np.argmax( bOut )
    choice = -1

    #Check if there are multiple indices.
    if ( indices.size > 1 ):
        choice = np.random.choice( indices )
    else:
        choice = indices

    #Check for converting center atom to +.
    if ( choice == 18 ):
        actions.append( { "convertAtom" : [] } )
    else:
        #Check for -.
        if ( mctx._CenterAtom._Value == "-" ):
            if ( choice < len( mctx._AtomCircle ) ):
                actions.append( { "minusAtom" : [ choice ] } )
        else:
            if ( choice <= len( mctx._AtomCircle ) ):
                actions.append( { "addAtom" : [ mctx._CenterAtom._Value, choice ] } )

    return actions

if __name__ == "__main__":
    Game.main()
