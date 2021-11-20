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
        self._MergedAtoms = []
        self._HighestAtom = 5
        self._Convertable = False

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

        if ( atom._Value == "-" ):
            self.minusAtom( index )
        else:
            self._AtomCircle.insert( index, atom )
            self._CenterAtom = self.GenerateAtom()
            self._Convertable = False

        self.mergeAtoms()

        if ( len( self._AtomCircle ) >= self._MaxAtoms ):
            self.GameOver()

    def mergeAtoms( self ):
        #Merge atoms with the same value on both sides of a '+' atom.
        index = 0
        while index != len(self._AtomCircle) and  len(self._AtomCircle) >= 3:
            if self._AtomCircle[index]._Value == '+':
                indexp1 = (index+1) % len(self._AtomCircle)
                indexm1 = (index-1) % len(self._AtomCircle)
                if self._AtomCircle[indexm1]._Value != self._AtomCircle[indexp1]._Value:
                    index += 1
                    continue

                self._MergedAtoms.append( { "center" : None, "surrounding" : [] } )
                self._MergedAtoms[len(self._MergedAtoms)-1]['center'] = self._AtomCircle[index]
                while self._AtomCircle[indexm1]._Value == self._AtomCircle[indexp1]._Value and \
                  (self._AtomCircle[indexm1]._Value != '+' and self._AtomCircle[indexm1] != '-') and \
                  len(self._AtomCircle) >= 3:
                    self._MergedAtoms[len(self._MergedAtoms)-1]['surrounding'].append( self._AtomCircle[indexp1] )

                    #Update score.
                    self._CurrentScore += self._AtomCircle[indexp1]._Value * 2 * len(self._MergedAtoms[len(self._MergedAtoms)-1]["surrounding"])

                    indexp1 = (index+1) % len(self._AtomCircle)
                    del self._AtomCircle[indexp1]

                    indexm1 = (index-1) % len(self._AtomCircle)
                    del self._AtomCircle[indexm1]

                    if index > indexm1:
                        index = (index-1) % len(self._AtomCircle)
                    indexp1 = (index+1) % len(self._AtomCircle)
                    indexm1 = (index-1) % len(self._AtomCircle)

                mergeValue = self._MergedAtoms[len(self._MergedAtoms)-1]["center"]._Value

                if ( mergeValue == '+' ):
                    mergeValue = 0

                prevValue = mergeValue
                for s in self._MergedAtoms[len(self._MergedAtoms)-1]["surrounding"]:
                    if ( mergeValue == 0 ):
                        mergeValue = s._Value + 1
                        prevValue = s._Value
                        continue

                    if ( prevValue >= s._Value ):
                        mergeValue += 1
                        prevValue = s._Value
                        continue

                    if ( prevValue < s._Value ):
                        mergeValue += s._Value - prevValue + 1
                        prevValue = s._Value
                        continue

                self._AtomCircle[index] = Atom( mergeValue )

                if ( mergeValue > self._HighestAtom ):
                    self._HighestAtom = mergeValue

                index = 0
            index += 1

    def minusAtom( self, index ):
        #Set the selected atom as the new center atom and remove it from the circle.
        self._CenterAtom = self._AtomCircle[index]
        self._Convertable = True
        del self._AtomCircle[index]

    def convertAtom( self ):
        #Convert the center atom into a plus atom.
        self._CenterAtom = Atom( "+" )

    def GenerateAtom( self ):
        #Probability distribution:
        #minus : 5%
        #plus  : 15%
        #1     : 15%
        #2     : 20%
        #3     : 20%
        #4     : 20%
        #5     : 5%
        avalue = random.randint(1, 100)

        if ( avalue <= 5 ):
            avalue = '-'
        elif ( avalue <= 20 ):
            avalue = '+'
        elif ( avalue <= 35 ):
            avalue = self._HighestAtom - 4
        elif ( avalue <= 55 ):
            avalue = self._HighestAtom - 3
        elif ( avalue <= 75 ):
            avalue = self._HighestAtom - 2
        elif ( avalue <= 95 ):
            avalue = self._HighestAtom - 1
        else:
            avalue = self._HighestAtom

        atom = Atom(avalue)
        return atom

    def GameOver( self ):
        print( "Game Over!" )
        print( "Score: " + str( self._CurrentScore ) )
        exit( 0 )

    class Context:
        def __init__( self, AtomCircle, CurrentScore, MaxAtoms, CenterAtom, MergedAtoms, HighestAtom, Convertable ):
            self._AtomCircle = copy.deepcopy( AtomCircle )
            self._CurrentScore = CurrentScore
            self._MaxAtoms = MaxAtoms
            self._CenterAtom = CenterAtom
            self._MergedAtoms = MergedAtoms
            self._HighestAtom = HighestAtom
            self._Convertable = Convertable

        def __str__( self ):
            ContextString = "Current Score: " + str( self._CurrentScore ) + "\n"
            ContextString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"

            for i, atom in enumerate( self._AtomCircle ):
                ContextString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

            return ContextString

        def __repr__( self ):
            return "Game.Context( AtomCircle, CurrentScore, MaxAtoms )"

    def MachineContext( self ):
        ctx = StateMachine.Context( self._AtomCircle, self._CurrentScore, self._MaxAtoms, self._CenterAtom, self._MergedAtoms, self._HighestAtom, self._Convertable )
        return ctx

    def input( self, commands ):
        self._MergedAtoms = []
        for cmdlist in commands:
            for cmd in cmdlist:
                utils.applyattr(self, cmd, cmdlist[cmd])


if __name__ == "__main__":
    Game.main()
