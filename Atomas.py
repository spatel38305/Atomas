#!/usr/bin/env python3

class Atom:
    def __init__( self, value, element ):
        self._value = value
        self._element = element

    def __str__( self ):
        return "Atom value: " + str( self._value ) + ", Atom element: " + str( self._element )

    def __repr__( self ):
        return "Atom( " + str( self._value ) + ", " + str( self._element ) + " )"

def main():
    a = Atom( 1, "H" )
    print( str( a ) )
    print( repr( a ) )

if __name__ == "__main__":
    main()
