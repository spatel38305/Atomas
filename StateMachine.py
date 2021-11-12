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
        return "Atom(" + str( self._Value ) + ")"

class StateMachine:
    def __init__( self, MaxAtoms ):
        self._CurrentScore = 0
        self._MaxAtoms = MaxAtoms
        self._AtomCircle = []
        self._CenterAtom = Atom(0)
        self._MergedAtoms = {'center': None, 'surrounding': 0}

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
        self._CenterAtom = self.GenerateAtom()

        self.mergeAtoms()
        if ( atom._Value == "-" ):
            self.minusAtom( index )

        if ( len( self._AtomCircle ) >= self._MaxAtoms ):
            self.GameOver()

    def mergeAtoms( self ):
        #Todo: can have multiple "center"/"surroudning" atoms due to more complex chaining of atoms
        index = 0
        while index != len(self._AtomCircle) and  len(self._AtomCircle) >= 3:
            if self._AtomCircle[index]._Value == '+':
                indexp1 = (index+1) % len(self._AtomCircle)
                indexm1 = (index-1) % len(self._AtomCircle)
                if self._AtomCircle[indexm1]._Value != self._AtomCircle[indexp1]._Value:
                    index += 1
                    continue
                
                self._MergedAtoms['center'] = index
                while self._AtomCircle[indexm1]._Value == self._AtomCircle[indexp1]._Value and \
                  (self._AtomCircle[indexm1]._Value != '+' and self._AtomCircle[indexm1] != '-') and \
                  len(self._AtomCircle) >= 3:
                    self._MergedAtoms['surrounding'] += 1
                    
                    indexp1 = (index+1) % len(self._AtomCircle)
                    del self._AtomCircle[indexp1]

                    indexm1 = (index-1) % len(self._AtomCircle)
                    del self._AtomCircle[indexm1]
                    
                    if index > indexm1:
                        index = (index-1) % len(self._AtomCircle)
                    indexp1 = (index+1) % len(self._AtomCircle)
                    indexm1 = (index-1) % len(self._AtomCircle)
                del self._AtomCircle[index]
                index = 0
            index += 1

    def minusAtom( self, index ):
        #TODO get the atom to be removed

        print( "Minusing" )

    def GenerateAtom( self ):
        #TODO based on score and normal distribution, generate new atom
        avalue = random.randint(0,5)
        if avalue == 4:
            avalue = '+'
        if avalue == 3:
            avalue = '-'

        atom = Atom(avalue)
        return atom

    def GameOver( self ):
        print( "Game Over!" )
        exit( 0 )

    class Context:
        def __init__( self, AtomCircle, CurrentScore, MaxAtoms, CenterAtom, MergedAtoms ):
            self._AtomCircle = copy.deepcopy( AtomCircle )
            self._CurrentScore = CurrentScore
            self._MaxAtoms = MaxAtoms
            self._CenterAtom = CenterAtom
            self._MergedAtoms = MergedAtoms

        def __str__( self ):
            ContextString = "Current Score: " + str( self._CurrentScore ) + "\n"
            ContextString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"
            
            for i, atom in enumerate( self._AtomCircle ):
                ContextString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

            return ContextString

        def __repr__( self ):
            return "Game.Context( AtomCircle, CurrentScore, MaxAtoms )"

    def MachineContext( self ):
        ctx = StateMachine.Context( self._AtomCircle, self._CurrentScore, self._MaxAtoms, self._CenterAtom, self._MergedAtoms )
        return ctx

    def input( self, commands ):
        self._MergedAtoms = {'center': None, 'surrounding': 0}
        for cmdlist in commands:
            for cmd in cmdlist:
                utils.applyattr(self, cmd, cmdlist[cmd])


if __name__ == "__main__":
    Game.main()
