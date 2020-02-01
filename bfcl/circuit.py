"""Circuit gate data structure.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest

from bfcl.gate import Gate

class Circuit():
    """
    Class for circuits.
    
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
    
    """

    def __init__(self, raw = None):
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
            gateNew = Gate()

            gateNew.wire_in_count = int(tokens[0])
            gateNew.wire_out_count = int(tokens[1])

            switch = 2 + gateNew.wire_in_count
            gateNew.wire_in_index = [int(t) for t in tokens[2:switch]]
            gateNew.wire_out_index = [int(t) for t in tokens[switch:-1]]
            gateNew.operation =\
              Gate.operation_from_bristol_fashion_string(tokens[-1])

            self.gate.append(gateNew);

if __name__ == "__main__":
    doctest.testmod()
