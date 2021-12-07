import Game
import numpy as np

def getRandomAction( mctx ):
    smi = []
    possibleActions = [ i for i in range( len( mctx._AtomCircle ) ) ]

    if mctx._Convertable == True:
        possibleActions.append( len( mctx._AtomCircle ) )

    if ( len( possibleActions ) == 0 ):
        return [ { "addAtom" : [ mctx._CenterAtom._Value, 0 ] } ]

    action = np.random.choice( possibleActions )

    if action == len( mctx._AtomCircle ):
        smi.append( { "convertAtom" : [] } )
    else:
        if ( mctx._CenterAtom._Value == "-" ):
            smi.append( { "minusAtom" : [ action ] } )
        else:
            smi.append( { "addAtom" : [ mctx._CenterAtom._Value, action ] } )

    return smi

if __name__ == "__main__":
    games = []
    numGames = 1000000

    scores = np.ndarray( ( numGames ) )

    for i in range( numGames ):
        games.append( Game.Game(**{'render': False}) )

    for i, g in enumerate( games ):
        while ( True ):
            mctx = g.stateMachine.MachineContext()

            if mctx._Running == False:
                scores[i] = mctx._CurrentScore
                break

            smi = getRandomAction( mctx )

            mctx = g.runTick( smi )

            if mctx._Running == False :
                scores[i] = mctx._CurrentScore
                break
        if ( ( ( i + 1 ) % 10000 ) == 0 ):
            print( "Finished %d games." % ( i + 1 ) )

    average = np.average( scores )
    print( "Average : %.6f" % ( average ) )

    max = np.amax( scores )
    print( "Max score: %d" % ( max ) )
