#!/usr/bin/env python3

class Atom:
    def __init__( self, value, element ):
        self._Value = value
        self._Element = element

    def __str__( self ):
        return "Atom value: " + str( self._Value ) + ", Atom element: " + str( self._Element )

    def __repr__( self ):
        return "Atom( " + str( self._Value ) + ", " + str( self._Element ) + " )"

class Game:
    def __init__( self, MaxAtoms ):
        self._CurrentScore = 0
        self._MaxAtoms = 18
        self._AtomCircle = []

    def __str__( self ):
        GameStateString = "Current Score: " + str( self._CurrentScore ) + "\n"
        GameStateString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"
        
        for i, atom in enumerate( self._AtomCircle ):
            GameStateString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

        return GameStateString

    def __repr__( self ):
        return "Game( " + str( self._MaxAtoms ) + " )"

    def addAtom( self, atom, index ):
        self._AtomCircle.insert( index, atom )

        if ( atom._Element == "+" ):
            self.mergeAtoms( index )
        elif ( atom._Element == "-" ):
            self.minusAtom( index )

        if ( len( self._AtomCircle ) >= self._MaxAtoms ):
            self.GameOver()

    def mergeAtoms( self, index ):
        #TODO check adjacent atoms and merge as necessary
        #TODO merge iteratively multiple times or maybe merge recursively

        print( "Merging" )

    def minusAtom( self, index ):
        #TODO get the atom to be removed
        #TODO change it into a plus or place it elsewhere

        print( "Minusing" )

    def GameOver( self ):
        print( "Game Over!" )
        exit( 1 )

def main():
    a = Atom( 1, "H" )
    print( str( a ) )
    print( repr( a ) )
    print()

    g = Game( 18 )
    print( str( g ) )
    print( repr( g ) )
    print()

    g.addAtom( a, 0 )
    print( str( g ) )
    print()

    a = Atom( 0, "+" )
    g.addAtom( a, 100 )
    print( str( g ) )
    print()

    a = Atom( 0, "-" )
    g.addAtom( a, 100 )
    print( str( g ) )
    print()

if __name__ == "__main__":
    main()
