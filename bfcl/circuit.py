"""Circuit gate data structure.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest

from bfcl.gate import Gate

class Circuit():
    """
    Data structure for circuits.
    
    >>> circuit_string = ['7 36', '2 4 4', '1 1']
    >>> circuit_string.extend(['2 1 0 1 15 AND', '2 1 2 3 16 AND'])
    >>> circuit_string.extend(['2 1 15 16 8 AND', '2 1 4 5 22 AND'])
    >>> circuit_string.extend(['2 1 6 7 23 AND', '2 1 22 23 9 AND'])
    >>> circuit_string.extend(['2 1 8 9 35 AND'])
    >>> c = Circuit()
    >>> c.parse_from_bristol_fashion_string("\\n".join(circuit_string))
    >>> c.gate_count
    7
    >>> c.wire_count
    36
    >>> c.value_in_count
    2
    >>> c.value_in_length
    [4, 4]
    >>> c.value_out_count
    1
    >>> c.wire_in_count
    8
    >>> c.wire_in_index
    [0, 1, 2, 3, 4, 5, 6, 7]
    >>> c.wire_out_count
    1
    >>> c.wire_out_index
    [35]
    >>> (c.gate[0].wire_in_index, c.gate[0].wire_out_index)
    ([0, 1], [15])
    >>> (c.gate[1].wire_in_index, c.gate[1].wire_out_index)
    ([2, 3], [16])
    >>> (c.gate[2].wire_in_index, c.gate[2].wire_out_index)
    ([15, 16], [8])
    >>> (c.gate[3].wire_in_index, c.gate[3].wire_out_index)
    ([4, 5], [22])
    >>> (c.gate[4].wire_in_index, c.gate[4].wire_out_index)
    ([6, 7], [23])
    >>> (c.gate[5].wire_in_index, c.gate[5].wire_out_index)
    ([22, 23], [9])
    >>> (c.gate[6].wire_in_index, c.gate[6].wire_out_index)
    ([8, 9], [35])
    >>> {c.gate[i].operation for i in range(7)}
    {'AND'}
    >>> from itertools import product
    >>> inputs = list(product(*([[0,1]]*4)))
    >>> pairs = product(inputs, inputs)
    >>> outputs = ([0]*255) + [1]
    >>> [c.evaluate(p)[0][0] for p in pairs] == outputs
    True
    """

    def __init__(self, raw = None):
        """Initialize a circuit data structure instance."""
        self.gate_count = 0
        self.wire_count = 0
        self.value_in_count = 0
        self.value_in_length = []
        self.value_out_count = 0
        self.value_out_length = []

        # The four fields below are technically redundant but included
        # to support cleaner algorithm implementations.
        self.wire_in_count = 0
        self.wire_in_index = []
        self.wire_out_count = 0
        self.wire_out_index = []

        self.gate = []
        
        if raw is not None:
            self.parse_from_bristol_fashion_string(raw)

    def parse_from_bristol_fashion_string(self, raw):
        """Parse a Bristol Fashion string representation of a circuit."""
        rows = [r.strip() for r in raw.split("\n") if r.strip() != ""]
        rows = [[tok.strip() for tok in r.split(" ")] for r in rows]

        self.gate_count = int(rows[0][0])
        self.wire_count = int(rows[0][1])

        # Determine total number of input and output wires.
        self.wire_in_count = 0
        self.wire_out_count = 0
        for i in range(1, len(rows[1])):
            length = int(rows[1][i])
            self.value_in_count += 1
            self.value_in_length.append(length)
            self.wire_in_count += length
        for i in range(1, len(rows[2])):
            length = int(rows[2][i])
            self.value_out_count += 1
            self.value_out_length.append(length)
            self.wire_out_count += length

        # Collect input/output wire indices for easier processing.
        for i in range(0, self.wire_in_count):
            self.wire_in_index.append(i)

        for i in range(self.wire_count-self.wire_out_count, self.wire_count):
            self.wire_out_index.append(i)

        # Parse the individual gates.
        for row in range(3, self.gate_count+3):
            tokens = rows[row]
            gate_new = Gate()

            gate_new.wire_in_count = int(tokens[0])
            gate_new.wire_out_count = int(tokens[1])

            switch = 2 + gate_new.wire_in_count
            gate_new.wire_in_index = [int(t) for t in tokens[2:switch]]
            gate_new.wire_out_index = [int(t) for t in tokens[switch:-1]]
            gate_new.operation =\
              Gate.operation_from_bristol_fashion_string(tokens[-1])

            self.gate.append(gate_new)

    def evaluate(self, inputs):
        """Evaluate a circuit on a sequence of input bit vectors."""
        wire = [0 for _ in range(self.wire_count)]
        circuit_input_wire_index = 0

        # Assign input values to corresponding wires.
        # It is assumed that the number of input wires
        # in the circuit matches the total number of bits
        # across all inputs in the inputs vector.
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                wire[circuit_input_wire_index] = inputs[i][j]
                circuit_input_wire_index += 1

        # Evaluate the gates.
        for i in range(self.gate_count):
            if self.gate[i].operation == 'NOT':
                wire[self.gate[i].wire_out_index[0]] =\
                    0 if\
                    (wire[self.gate[i].wire_in_index[0]] == 1)\
                    else 1
            elif self.gate[i].operation == 'AND':
                wire[self.gate[i].wire_out_index[0]] =\
                    1 if\
                    ((wire[self.gate[i].wire_in_index[0]] == 1) and\
                     (wire[self.gate[i].wire_in_index[1]] == 1))\
                    else 0
            elif self.gate[i].operation == 'XOR':
                wire[self.gate[i].wire_out_index[0]] =\
                    1 if\
                    (wire[self.gate[i].wire_in_index[0]] !=\
                     wire[self.gate[i].wire_in_index[1]])\
                    else 0
            elif self.gate[i].operation == 'OR':
                wire[self.gate[i].wire_out_index[0]] =\
                    1 if\
                    ((wire[self.gate[i].wire_in_index[0]] == 1) or\
                     (wire[self.gate[i].wire_in_index[1]] == 1))\
                    else 0
            elif self.gate[i].operation == 'NAND':
                wire[self.gate[i].wire_out_index[0]] =\
                    0 if\
                    ((wire[self.gate[i].wire_in_index[0]] == 1) and\
                     (wire[self.gate[i].wire_in_index[1]] == 1))\
                    else 1
            elif self.gate[i].operation == 'NIMP':
                wire[self.gate[i].wire_out_index[0]] =\
                    1 if\
                    ((wire[self.gate[i].wire_in_index[0]] == 1) and\
                     (wire[self.gate[i].wire_in_index[1]] == 0))\
                    else 0
            elif self.gate[i].operation == 'UNKNOWN':
                pass

        # Build the output values.
        outputs = []
        offset = self.wire_count
        for i in range(self.value_out_count):
            offset -= self.value_out_length[i]
        for i in range(self.value_out_count):
            bits = []
            for j in range(self.value_out_length[i]):
                bits.append(wire[offset])
                offset += 1
            outputs.append(bits)

        return outputs

if __name__ == "__main__":
    doctest.testmod()
