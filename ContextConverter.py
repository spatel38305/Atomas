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

if __name__ == "__main__":
    Game.main()
