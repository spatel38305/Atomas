#!/usr/bin/env python3

from StateMachine import *
import itertools
import timeit
import argparse
import copy

def addAtomWithoutMerge( s, atom, index ):
    atom = Atom(atom)

    s._AtomCircle.insert( index, atom )

def addAllAtoms( s, atoms ):
    for a in atoms:
        addAtomWithoutMerge( s, a, 0 )

def deleteAllAtoms( s ):
    for i in range( len( s._AtomCircle ) ):
        del s._AtomCircle[0]

def testMergePermutations( n ):
    maxAtoms = 18
    minLen = 3
    atomValues = [ 1, 2, "+" ]
    s = StateMachine( maxAtoms )

    if ( n < minLen ):
        print( "n (%d) must be greater than minLen (%d)" % ( n, minLen ) )
        exit( 1 )

    numPermutations = 0
    failed = 0

    for p in itertools.product( atomValues, repeat = n ):
        numPermutations += 1

        try:
            addAllAtoms( s, p )
            atomCircleCopy = copy.deepcopy( s._AtomCircle )
            s.checkMerge()
        except Exception as err:
            print( "FAILED!" )
            print( atomCircleCopy )
            print( err )
            print()
            failed += 1

        deleteAllAtoms( s )

    print( "For n = %d : %d permutations - FAILED : %d" % ( n, numPermutations, failed ) )

    return numPermutations, failed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "-n", dest = "n", required = True )

    args = parser.parse_args()

    n = int( args.n )

    if ( ( n < 3 ) or ( n > 18 ) ):
        print( "n (%d) must be 3 to 18" % ( n ) )
        exit( 1 )

    totalPermutations = 0
    totalFailed = 0
    minLen = 3
    maxAtoms = n

    totalTime = timeit.default_timer()

    for i in range( minLen, maxAtoms + 1 ):
        startTime = timeit.default_timer()

        p, f = testMergePermutations( i )
        totalPermutations += p
        totalFailed += f

        print( "Time for n = %d : %f" % ( i, timeit.default_timer() - startTime ) )

    print( "Total permutations : %d - Total FAILED : %d" % ( totalPermutations, totalFailed ) )
    print( "Total time : %f" % ( timeit.default_timer() - totalTime ) )
