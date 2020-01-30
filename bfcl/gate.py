"""Circuit data structure.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest

class Gate():
    """
    Class for circuit gates.
    """

    def __init__(self):
        wire_in_index = []
        wire_out_index = []
        operation = 'UNKNOWN'
    
    @staticmethod
    def operation_from_bristol_fashion_string(raw):
        convert = {'AND':'AND', 'XOR':'XOR', 'INV':'NOT'}
        return convert[raw.upper().strip()]

if __name__ == "__main__":
    doctest.testmod()
