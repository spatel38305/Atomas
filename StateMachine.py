#!/usr/bin/env python3
import copy
import random

import Game
import utils

class Atom:
    def __init__( self, value ):
        self._Value = value

    def __str__( self ):
        return "Atom value: " + str( self._Value )

    def __repr__( self ):
        return "Atom( " + str( self._Value )

class StateMachine:
    def __init__( self, MaxAtoms ):
        self._CurrentScore = 0
        self._MaxAtoms = MaxAtoms
        self._AtomCircle = []
        self._CenterAtom = Atom(0)

    def __str__( self ):
        GameStateString = "Current Score: " + str( self._CurrentScore ) + "\n"
        GameStateString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"
        
        for i, atom in enumerate( self._AtomCircle ):
            GameStateString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

        return GameStateString

    def __repr__( self ):
        return "StateMachine( " + str( self._MaxAtoms ) + " )"

    def addAtom( self, atom, index ):
        try:
            if ( atom is None ):
                raise Exception( "atom is None" )
            if ( index > len(self._AtomCircle)):
                raise Exception( "added out of bounds index" )
        except Exception as exc:
            print( exc )
            print( "atom should not be None" )
            print( "DYING NOW!" )
            exit( 1 )

        self._AtomCircle.insert( index, atom )
        self._CenterAtom = Atom(random.randint(0,5))

        if ( atom._Value == "+" ):
            self.mergeAtoms( index )
        elif ( atom._Value == "-" ):
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
        atom = Atom(random.randInt(0,5))

        return atom

    def GameOver( self ):
        print( "Game Over!" )
        exit( 0 )

    class Context:
        def __init__( self, AtomCircle, CurrentScore, MaxAtoms, CenterAtom ):
            self._AtomCircle = copy.deepcopy( AtomCircle )
            self._CurrentScore = CurrentScore
            self._MaxAtoms = MaxAtoms
            self._CenterAtom = CenterAtom

        def __str__( self ):
            ContextString = "Current Score: " + str( self._CurrentScore ) + "\n"
            ContextString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"
            
            for i, atom in enumerate( self._AtomCircle ):
                ContextString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

            return ContextString

        def __repr__( self ):
            return "Game.Context( AtomCircle, CurrentScore, MaxAtoms )"

    def MachineContext( self ):
        ctx = StateMachine.Context( self._AtomCircle, self._CurrentScore, self._MaxAtoms, self._CenterAtom )
        return ctx

    def input( self, commands ):
        for cmdlist in commands:
            for cmd in cmdlist:
                utils.applyattr(self, cmd, cmdlist[cmd])


if __name__ == "__main__":
    Game.main()
