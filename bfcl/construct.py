"""Circuit construction combinators.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest
from parts import parts

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

        return gate_new.wire_out_index
        
    def gates_map(self, operation, wire_in_index):
        wire_out_index = []
        for i in wire_in_index:
            wire_out_index.append(self.gate(operation, i))
        return wire_out_index

    def gates_zip(self, operation, wire_in_index_lft, wire_in_index_rgt):
        wire_out_index = []
        for (l, r) in zip(wire_in_index_lft, wire_in_index_rgt):
            wire_out_index.append(self.gate(operation, l, r))
        return wire_out_index

    def gates_pair(self, operation, wire_in_index):
        wire_out_index = []
        for ws in parts(wire_in_index, length=2):
            if len(ws) == 1:
                wire_out_index.append(ws[0])
            else:
                wire_out_index.append(self.gate(operation, ws[0], ws[1]))
        return wire_out_index

    def gates_fold(self, operation, wire_in_index):
        wire_out_index = self.gates_pair(operation, wire_in_index)
        while len(wire_out_index) > 1:
            wire_out_index = self.gates_pair(operation, wire_out_index)
        return wire_out_index[0]

if __name__ == "__main__":
    doctest.testmod()
