"""Circuit definition data structures.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

from __future__ import annotations
from typing import Sequence
import doctest
from parts import parts
import circuit as circuit_

class operation(circuit_.operation):
    """
    Data structure for an individual gate operation.
    """

    @staticmethod
    def parse(token: str) -> operation:
        """Parse a Bristol Fashion circuit gate operator token."""
        return dict(operation.token_op_pairs).get(token.upper().strip())

    def emit(self: operation) -> str:
        """Emit a Bristol Fashion operation token."""
        return [s for (s, o) in operation.token_op_pairs if o == self][0]

operation.token_op_pairs = [
    ('LID', operation((0,1))),
    ('INV', operation((1,0))),
    ('FLS', operation((0,0,0,0))),
    ('AND', operation((0,0,0,1))),
    ('NIM', operation((0,0,1,0))),
    ('FST', operation((0,0,1,1))),
    ('NIF', operation((0,1,0,0))),
    ('SND', operation((0,1,0,1))),
    ('XOR', operation((0,1,1,0))),
    ('LOR', operation((0,1,1,1))),
    ('NOR', operation((1,0,0,0))),
    ('XNR', operation((1,0,0,1))),
    ('NSD', operation((1,0,1,0))),
    ('LIF', operation((1,0,1,1))),
    ('NFT', operation((1,1,0,0))),
    ('IMP', operation((1,1,0,1))),
    ('NND', operation((1,1,1,0))),
    ('TRU', operation((1,1,1,1)))
]

# Concise synonym for class.
op = operation

class gate():
    """
    Data structure for an individual circuit logic gate.
    """

    def __init__(
            self: gate,
            wire_in_count: int = None, wire_out_count: int = None,
            wire_in_index: Sequence[int] = None,
            wire_out_index: Sequence[int] = None,
            operation: operation = None
        ):
        self.wire_in_count = wire_in_count
        self.wire_out_count = wire_out_count
        self.wire_in_index = [] if wire_in_index is None else wire_in_index
        self.wire_out_index = [] if wire_out_index is None else wire_out_index
        self.operation = operation

    @staticmethod
    def parse(tokens) -> gate:
        """Parse a Bristol Fashion gate string or token list."""
        if isinstance(tokens, str):
            tokens = [tok.strip() for tok in tokens.strip().split(" ")]

        return gate(
            int(tokens[0]), int(tokens[1]),
            [int(t) for t in tokens[2: 2+int(tokens[0])]],
            [int(t) for t in tokens[2+int(tokens[0]):-1]],
            operation.parse(tokens[-1])
        )

    def emit(self: gate) -> str:
        """Emit a Bristol Fashion string for this gate."""
        return " ".join([
            str(self.wire_in_count), str(self.wire_out_count),
            " ".join([str(i) for i in self.wire_in_index]),
            " ".join([str(i) for i in self.wire_out_index]),
            self.operation.emit()
        ])

class circuit():
    """
    Data structure for circuits.

    >>> circuit_string = ['7 36', '2 4 4', '1 1']
    >>> circuit_string.extend(['2 1 0 1 15 AND', '2 1 2 3 16 AND'])
    >>> circuit_string.extend(['2 1 15 16 8 AND', '2 1 4 5 22 AND'])
    >>> circuit_string.extend(['2 1 6 7 23 AND', '2 1 22 23 9 AND'])
    >>> circuit_string.extend(['2 1 8 9 35 AND'])
    >>> circuit_string = "\\n".join(circuit_string)
    >>> c = circuit()
    >>> c.parse(circuit_string)
    >>> c.emit() == circuit_string
    True
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
    >>> {c.gate[i].operation for i in range(7)} == {op.and_}
    True
    >>> from itertools import product
    >>> inputs = list(product(*([[0,1]]*4)))
    >>> pairs = product(inputs, inputs)
    >>> outputs = ([0]*255) + [1]
    >>> [c.evaluate(p)[0][0] for p in pairs] == outputs
    True
    """

    def __init__(self: circuit, raw=None):
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

        # Convert a string or circuit input.
        if isinstance(raw, str):
            self.parse(raw)
        elif isinstance(raw, circuit_.circuit):
            self.circuit(raw)

    def circuit(self: circuit, c: circuit_.circuit):
        """Construct a Bristol Fashion circuit from `circuit` library object."""
        sig = c.signature
        self.gate_count =\
            c.count(lambda g: not (len(g.inputs) == 0 and len(g.outputs) > 0))
        self.wire_count = len(c.gate)
        self.value_in_count =\
            1 if sig.input_format is None else len(sig.input_format)
        self.value_in_length =\
            [self.wire_count - self.gate_count]\
            if sig.input_format is None else\
            sig.input_format
        self.value_out_count =\
            1 if sig.output_format is None else len(sig.output_format)
        self.value_out_length =\
            [c.count(lambda g: len(g.outputs) == 0)]\
            if sig.output_format is None else\
            sig.output_format

        self.wire_in_count = self.wire_count - self.gate_count
        self.wire_in_index = list(range(0, self.wire_in_count))
        self.wire_out_count = c.count(lambda g: len(g.outputs) == 0)
        self.wire_out_index =\
            list(range(self.wire_count - self.wire_out_count, self.wire_count))

        self.gate = []
        for i in range(len(c.gate)):
            if len(c.gate[i].inputs) > 0:
                self.gate.append(gate(
                    len(c.gate[i].inputs), 1,
                    [ig.index for ig in c.gate[i].inputs], [c.gate[i].index],
                    operation(c.gate[i].operation)
                ))

    def parse(self: circuit, raw: str):
        """Parse a Bristol Fashion string representation of a circuit."""
        rows = [
            [tok.strip() for tok in r.strip().split(" ")]
            for r in raw.split("\n") if r.strip() != ""
        ]

        self.gate_count = int(rows[0][0])
        self.wire_count = int(rows[0][1])

        # Determine total number of input and output wires.
        self.wire_in_count = 0
        for i in range(1, len(rows[1])):
            length = int(rows[1][i])
            self.value_in_count += 1
            self.value_in_length.append(length)
            self.wire_in_count += length

        self.wire_out_count = 0
        for i in range(1, len(rows[2])):
            length = int(rows[2][i])
            self.value_out_count += 1
            self.value_out_length.append(length)
            self.wire_out_count += length

        # Collect input/output wire indices for easier processing.
        self.wire_in_index = list(range(0, self.wire_in_count))
        self.wire_out_index =\
            list(range(self.wire_count-self.wire_out_count, self.wire_count))

        # Parse the individual gates.
        self.gate = [gate.parse(row) for row in rows[3:self.gate_count+3]]

    def emit(self: circuit, progress=lambda _: _) -> str:
        """Emit a Bristol Fashion circuit definition."""
        lines = [
            [str(self.gate_count), str(self.wire_count)],
            [str(self.value_in_count)] + list(map(str, self.value_in_length)),
            [str(self.value_out_count)] + list(map(str, self.value_out_length))
        ]
        lines.extend([[g.emit()] for g in progress(self.gate)])
        return "\n".join(" ".join(line) for line in lines)

    def evaluate(
            self: circuit,
            inputs: Sequence[Sequence[int]]
        ) -> Sequence[Sequence[int]]:
        """Evaluate a circuit on a sequence of input bit vectors."""

        # It is assumed that the number of input wires in the circuit matches
        # the total number of bits across all inputs in the inputs vector.
        inputs = [b for bs in inputs for b in bs]
        wire = inputs + [0]*(self.wire_count-len(inputs))

        # This total is useful in case output wire indices are absent.
        wire_in_count = len(inputs)

        # Evaluate the gates.
        for (ig, g) in enumerate(self.gate):
            # If no output wire index is present, use the gate count as the index.
            wire_out_index =\
                g.wire_out_index[0] if hasattr(g, 'wire_out_index') else\
                wire_in_count + ig

            # Compute the operation and store the result.
            wire[wire_out_index] =\
                g.operation(*[wire[i] for i in g.wire_in_index])

        # Format and return the output bit vectors.
        return list(parts(
            wire[-self.wire_out_count:],
            length=self.value_out_length
        ))

if __name__ == "__main__":
    doctest.testmod()
