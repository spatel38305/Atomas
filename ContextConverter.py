import numpy as np
from StateMachine import *
from collections import defaultdict
import Game


def convertContext_0( mctx ):
    '''
    20 inputs
    each potential atom location (1-18) is an input with the value being the atom at the respective location
    2 extra inputs for if an atom is convertable and if the center atom is a plus or minus for a total of 20 inputs
    '''
    x = np.full( ( 20 ), 0 )
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
        v = -1 if a._Value == '+' else a._Value
        x[i + 2] = v

    y[0] = mctx._CurrentScore + mctx._TotalThrown

    return x, y

def convertContext_1(mctx):
    '''
    20 inputs
    each potential atom location (1-18) is an input with the value being a unique integer representing that atom
    2 extra inputs for if an atom is convertable and if the center atom is a plus or minus for a total of 20 inputs
    '''
    x = np.full( ( 20 ), 0 )
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

    atomCircle = map(lambda x: -1 if x._Value == '+' else x._Value, mctx._AtomCircle)

    temp = defaultdict(lambda: len(temp))
    res = [temp[ele] for ele in atomCircle]

    for i, a in enumerate( res ):
        x[i + 2] = a

    y[0] = mctx._CurrentScore + mctx._TotalThrown

    return x, y

def convertContext_2(mctx):
    '''
        119*18 + 4 = 2128 inputs
        There are 119 inputs, each representing a unique atom. Like-valued inputs can be merged together.
        This value can be reduced to say, 30 inputs, where we modulo the atom value by 30. This, in effect,
        would treat the 0th atom and 30th atom as the same atom, but we should not have 2 atoms 30 values apart in
        a single circle. This must be repeated for each potential slot, effectively binarizing, vectorizing, or one-hot-encoding
        the input into the large category space of potential atoms.
    '''
    size = 119
    x = np.full( ( size, 18 ), 0 )
    y = np.ndarray( ( 1 ) )

    for i, n in enumerate(mctx._AtomCircle):
        x[n._Value if n._Value != "+" else 0,i] = 1

    x = x.flatten()

    if ( mctx._Convertable == True ):
        x = np.append(x, 1)
    else:
        x = np.append(x, 0)

    if ( mctx._CenterAtom._Value == '+' ):
        x = np.append(x, 1)
    else:
        x = np.append(x, 0)

    if( mctx._CenterAtom._Value == '-' ):
        x = np.append(x, 1)
    else:
        x = np.append(x, 0)

    if( mctx._CenterAtom._Value != '+' and mctx._CenterAtom._Value != '-' ):
        x = np.append(x, mctx._CenterAtom._Value)
    else:
        x = np.append(x, 0)


    y[0] = mctx._CurrentScore + mctx._TotalThrown
    return x, y

def convertContext_3( mctx ):
    '''
    22 inputs
    Same as Convert Context 1 but forwards ALL of the information from mctx to see if that improves performance any
    mctx: MergedAtoms, HighestAtom
    '''
    x = np.full( ( 18 + 2 + 2 ), 0 )
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
        v = -1 if a._Value == '+' else a._Value
        x[i + 2] = v

    x[20] = len(mctx._MergedAtoms)
    x[21] = mctx._HighestAtom

    y[0] = mctx._CurrentScore + mctx._TotalThrown

    return x, y

def convertContext(version, mctx):
    '''
    driver code for calling correct corresponding context converter based on current mode (version)
    '''
    if version == 0:
        return convertContext_0(mctx)
    elif version == 1:
        return convertContext_1(mctx)
    elif version == 2:
        return convertContext_2(mctx)
    elif version == 3:
        return convertContext_3(mctx)

def convertOutput( bOut, mctx ):
    '''
    The output converter to translate the AI output back into instructions the state machine can understand
    '''
    actions = []
    indices = np.argmax( bOut )
    choice = -1

    #Check if there are multiple indices.
    if ( indices.size > 1 ):
        choice = np.random.choice( indices )
    else:
        choice = indices

    #Check for converting center atom to +.
    if ( choice == 18 ):
        actions.append( { "convertAtom" : [] } )
    else:
        #Check for -.
        if ( mctx._CenterAtom._Value == "-" ):
            if ( choice < len( mctx._AtomCircle ) ):
                actions.append( { "minusAtom" : [ choice ] } )
        else:
            if ( choice <= len( mctx._AtomCircle ) ):
                actions.append( { "addAtom" : [ mctx._CenterAtom._Value, choice ] } )

    return actions
