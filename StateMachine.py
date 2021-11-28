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
        self._Running = True
        self._CurrentScore = 0
        self._MaxAtoms = MaxAtoms
        self._AtomCircle = []
        self._CenterAtom = Atom(0)
        self._MergedAtoms = []
        self._HighestAtom = 5
        self._Convertable = False
        self._TotalThrown = 0

    def __str__( self ):
        GameStateString = "Current Score: " + str( self._CurrentScore ) + "\n"
        GameStateString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"

        for i, atom in enumerate( self._AtomCircle ):
            GameStateString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

        return GameStateString

    def __repr__( self ):
        return "StateMachine( " + str( self._MaxAtoms ) + " )"

    def addAtom( self, atom, index ):
        if ( atom is None ):
            raise Exception( "atom is None" )
        if ( index > len(self._AtomCircle)):
            raise Exception( "added out of bounds index" )
        atom = Atom(atom)

        self._AtomCircle.insert( index, atom )
        self._CenterAtom = self.GenerateAtom()
        self._Convertable = False
        self.checkMerge()

        if ( len( self._AtomCircle ) >= self._MaxAtoms ):
            self.GameOver()

        self._TotalThrown += 1

    def checkMerge( self ):
        index = 0
        largestMerge = 0
        mergeIndex = -1

        while ( ( len( self._AtomCircle ) >= 3 ) and ( index < len( self._AtomCircle ) ) ):

            if ( self._AtomCircle[index]._Value == '+' ):
                nindex = ( index + 1 ) % ( len( self._AtomCircle ) )
                pindex = ( index - 1 ) % ( len( self._AtomCircle ) )

                if ( self._AtomCircle[nindex]._Value != self._AtomCircle[pindex]._Value ):
                    index += 1
                    continue

                if ( ( self._AtomCircle[nindex]._Value == "+" ) or ( self._AtomCircle[pindex]._Value == "-" ) ):
                    index += 1
                    continue

                mCount = self.mergeCount( index )
                if ( mCount > largestMerge ):
                    largestMerge = mCount
                    mergeIndex = index

            index += 1

        if ( largestMerge != 0 ):
            self.mergeAtoms( mergeIndex, largestMerge )
            self.checkMerge()

    def mergeCount( self, index ):
        mCount = 0
        nCheck = index + 1
        pCheck = index - 1
        nindex = nCheck % len( self._AtomCircle )
        pindex = pCheck % len( self._AtomCircle )
        nAtom = self._AtomCircle[nindex]
        pAtom = self._AtomCircle[pindex]

        while ( ( ( nCheck - pCheck ) < len( self._AtomCircle ) ) and ( nAtom._Value == pAtom._Value ) and ( nAtom._Value != "+" ) and ( pAtom._Value != "-" ) ):
            mCount += 1
            nCheck += 1
            pCheck -= 1
            nindex = nCheck % len( self._AtomCircle )
            pindex = pCheck % len( self._AtomCircle )
            nAtom = self._AtomCircle[nindex]
            pAtom = self._AtomCircle[pindex]

        return mCount

    def mergeAtoms( self, index, largestMerge ):
        self._MergedAtoms.append( { "center" : None, "surrounding" : [] } )
        mindex = len( self._MergedAtoms ) - 1
        self._MergedAtoms[mindex]["center"] = self._AtomCircle[index]
        mCount = 0
        nindex = ( index + 1 ) % ( len( self._AtomCircle ) )
        pindex = ( index - 1 ) % ( len( self._AtomCircle ) )

        while ( mCount < largestMerge ):
            self._MergedAtoms[mindex]["surrounding"].append( self._AtomCircle[nindex] )

            #Update score.
            self._CurrentScore += self._AtomCircle[pindex]._Value * 2 * len( self._MergedAtoms[mindex]["surrounding"] )

            if ( nindex > pindex ):
                del self._AtomCircle[nindex]
                del self._AtomCircle[pindex]
            else:
                del self._AtomCircle[pindex]
                del self._AtomCircle[nindex]

            if ( index > pindex ):
                index = ( index - 1 ) % len( self._AtomCircle )

            nindex = ( index + 1 ) % ( len( self._AtomCircle ) )
            pindex = ( index - 1 ) % ( len( self._AtomCircle ) )
            mCount += 1

        mergeValue = self._MergedAtoms[mindex]["center"]._Value

        if ( mergeValue == "+" ):
            mergeValue = 0

        pMerge = mergeValue
        for s in self._MergedAtoms[mindex]["surrounding"]:

            if ( mergeValue == 0 ):
                mergeValue = s._Value + 1
                pMerge = s._Value
                continue

            if ( pMerge >= s._Value ):
                mergeValue += 1
                pMerge = s._Value
                continue

            if ( pMerge < s._Value ):
                mergeValue += s._Value - pMerge + 1
                pMerge = s._Value
                continue

        self._AtomCircle[index] = Atom( mergeValue )

        if ( mergeValue > self._HighestAtom ):
            self._HighestAtom = mergeValue

    def minusAtom( self, index ):
        #Set the selected atom as the new center atom and remove it from the circle.
        self._CenterAtom = self._AtomCircle[index]
        self._Convertable = True
        del self._AtomCircle[index]
        self.checkMerge()

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
        self._Running = False

    class Context:
        def __init__( self, Running, AtomCircle, CurrentScore, MaxAtoms, CenterAtom, MergedAtoms, HighestAtom, Convertable, TotalThrown ):
            self._Running = Running
            self._AtomCircle = copy.deepcopy( AtomCircle )
            self._CurrentScore = CurrentScore
            self._MaxAtoms = MaxAtoms
            self._CenterAtom = CenterAtom
            self._MergedAtoms = MergedAtoms
            self._HighestAtom = HighestAtom
            self._Convertable = Convertable
            self._TotalThrown = TotalThrown

        def __str__( self ):
            ContextString = "Current Score: " + str( self._CurrentScore ) + "\n"
            ContextString += "Current Atoms: " + str( len( self._AtomCircle ) ) + "\n"

            for i, atom in enumerate( self._AtomCircle ):
                ContextString += "Atom #" + str( i ) + ": " + str( atom ) + "\n"

            ContextString += "Center Atom: " + str( self._CenterAtom ) + "\n"

            return ContextString

        def __repr__( self ):
            return "Game.Context( AtomCircle, CurrentScore, MaxAtoms )"

    def MachineContext( self ):
        ctx = StateMachine.Context( self._Running, self._AtomCircle, self._CurrentScore, self._MaxAtoms, self._CenterAtom, self._MergedAtoms, self._HighestAtom, self._Convertable, self._TotalThrown )
        return ctx

    #debug
    def convertTo(self, idx, atom):
        if idx >= 0:
            self._AtomCircle[idx] = Atom(atom)
        elif idx == -1:
            self._CenterAtom = Atom(atom)

    def delete(self, idx):
        del self._AtomCircle[idx]

    def input( self, commands ):
        self._MergedAtoms = []
        for cmdlist in commands:
            for cmd in cmdlist:
                utils.applyattr(self, cmd, cmdlist[cmd])
        return self.MachineContext()


if __name__ == "__main__":
    Game.main()
