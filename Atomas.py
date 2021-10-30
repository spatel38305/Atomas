#!/usr/bin/env python3
import copy

import game

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
        try:
            if ( atom is None ):
                raise Exception( "atom is None" )
        except Exception as exc:
            print( exc )
            print( "atom should not be None" )
            print( "DYING NOW!" )
            exit( 1 )

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

        print( "Minusing" )

    def GenerateAtom( self ):
        #TODO based on score and normal distribution, generate new atom
        atom = Atom(0, 'H')

        return atom

    def GameOver( self ):
        print( "Game Over!" )
        exit( 0 )

    class Context:
        def __init__( self, AtomCircle, CurrentScore, MaxAtoms ):
            self._AtomCircle = copy.deepcopy( AtomCircle )
            self._CurrentScore = CurrentScore
            self._MaxAtoms = MaxAtoms

        def __str__( self ):
            ContextString = "Current Score: " + str( self._CurrentScore ) + "\n"
            ContextString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"
            
            for i, atom in enumerate( self._AtomCircle ):
                ContextString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

            return ContextString

        def __repr__( self ):
            return "Game.Context( AtomCircle, CurrentScore, MaxAtoms )"

    def MachineContext( self ):
        ctx = Game.Context( self._AtomCircle, self._CurrentScore, self._MaxAtoms )
        return ctx

if __name__ == "__main__":
    game.main()
