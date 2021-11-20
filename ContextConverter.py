import numpy as np

from StateMachine import *

import Game

class ContextConverter:
    def __init__( self ):
        self._mctx = None
        self._convertedMctx = None

    def __str__( self ):
        return "Content: " + str( self._mctx )

    def __repr__( self ):
        return "ContextConverter()"

    def updateContext( self, mctx ):
        self._mctx = mctx

    def convertContext( self ):
        x = np.ndarray( ( 20 ) )
        y = np.ndarray( ( 1 ) )

        if ( self._mctx._Convertable == True ):
            x[0] = 1
        else:
            x[0] = 0

        if ( self._mctx._CenterAtom._Value == '+' ):
            x[1] = -1
        elif( self._mctx._CenterAtom._Value == '-' ):
            x[1] = -2
        else:
            x[1] = self._mctx._CenterAtom._Value

        for i, a in enumerate( self._mctx._AtomCircle ):
            x[i + 2] = a._Value

        for i in range( 0, self._mctx._MaxAtoms - len( self._mctx._AtomCircle ) ):
            x[i + len( self._mctx._AtomCircle ) + 2] = 0

        y[0] = self._mctx._CurrentScore

        self._convertedMctx = ( x, y )

    def getConvertedContext( self ):
        return self._convertedMctx

if __name__ == "__main__":
    Game.main()
