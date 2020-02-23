"""Circuit construction combinators.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest

from bfcl.gate import Gate
from bfcl.circuit import Circuit

class Construct():
    """
    Class for circuit construction.
    """

    def __init__(self):
        self.circuit = Circuit()
        self.circuit.wire_count = 0
        self.circuit.value_in_count = 0
        self.circuit.value_in_length = []
        self.circuit.wire_in_count = 0
        self.circuit.wire_in_index = []
        self.circuit.gate = []
        
    def input(self, length):
        self.circuit.wire_count += length
    
        self.circuit.value_in_count += 1
        self.circuit.value_in_length.append(length)'

        wire_in_index_new = list(range(self.circuit.wire_in_count, self.circuit.wire_in_count + length))
        self.circuit.wire_in_count += length
        self.circuit.wire_in_index.extend(wire_in_index_new)

        return wire_in_index_new

    def gate(self, operation, wire_in_index_one, wire_in_index_two = None):
        gate_new = Gate()
        gate_new.operation = operation

        gate_new.wire_in_count = 1 if wire_in_index_two is None else 2
        gate_new.wire_out_count = 1
        gate_new.wire_in_index =\
            [wire_in_index_one] +\
            ([] if wire_in_index_two is None else [wire_in_index_two])

        gate_new.wire_out_index = [self.circuit.wire_count]
        self.circuit.wire_count += 1

        self.circuit.gate.append(gate_new)

        return gate_new

if __name__ == "__main__":
    doctest.testmod()
