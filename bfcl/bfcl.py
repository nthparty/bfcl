"""
Python library for working with circuit definitions
represented using the Bristol Fashion.
"""
from __future__ import annotations
from typing import Sequence, Union, Type
import doctest
from parts import parts
import circuit as circuit_

class operation(circuit_.operation):
    """
    Data structure for an individual gate operation. This class is derived
    from the :obj:`~logical.logical.logical` class exported by the
    `logical <https://pypi.org/project/logical/>`_ library. This module
    indirectly imports the :obj:`~logical.logical.logical` class via the
    :obj:`~circuit.circuit.op` synonym defined in the
    `circuit <https://pypi.org/project/circuit/>`_ library. See the
    documentation for the :obj:`~logical.logical.logical` class
    for more information on this data structure and how logical operations
    are represented as tuples of integers.
    """
    token_op_pairs = []
    """List of pairs of string representations and corresponding unary/binary operations."""

    @staticmethod
    def parse(token: str) -> operation:
        """
        Parse a Bristol Fashion circuit gate operator token.

        >>> operation.parse('AND')
        (0, 0, 0, 1)
        """
        return dict(operation.token_op_pairs).get(token.upper().strip())

    def emit(self: operation) -> str:
        """
        Emit a Bristol Fashion operation token.

        >>> operation((0, 1, 1, 0)).emit()
        'XOR'
        """
        return [s for (s, o) in operation.token_op_pairs if o == self][0]

operation.token_op_pairs = [
    ('LID', operation((0, 1))),
    ('INV', operation((1, 0))),
    ('FLS', operation((0, 0, 0, 0))),
    ('AND', operation((0, 0, 0, 1))),
    ('NIM', operation((0, 0, 1, 0))),
    ('FST', operation((0, 0, 1, 1))),
    ('NIF', operation((0, 1, 0, 0))),
    ('SND', operation((0, 1, 0, 1))),
    ('XOR', operation((0, 1, 1, 0))),
    ('LOR', operation((0, 1, 1, 1))),
    ('NOR', operation((1, 0, 0, 0))),
    ('XNR', operation((1, 0, 0, 1))),
    ('NSD', operation((1, 0, 1, 0))),
    ('LIF', operation((1, 0, 1, 1))),
    ('NFT', operation((1, 1, 0, 0))),
    ('IMP', operation((1, 1, 0, 1))),
    ('NND', operation((1, 1, 1, 0))),
    ('TRU', operation((1, 1, 1, 1)))
]

# Concise synonym for class.
op = operation

class gate():
    """
    Data structure for an individual circuit logic gate.

    >>> gate.parse('2 1 0 1 15 AND').emit()
    '2 1 0 1 15 AND'
    >>> gate.parse('1 1 100 200 INV').emit()
    '1 1 100 200 INV'
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
        """
        Parse a Bristol Fashion gate string or token list.
        """
        if isinstance(tokens, str):
            tokens = [tok.strip() for tok in tokens.strip().split(" ")]

        return gate(
            int(tokens[0]), int(tokens[1]),
            [int(t) for t in tokens[2: 2+int(tokens[0])]],
            [int(t) for t in tokens[2+int(tokens[0]):-1]],
            operation.parse(tokens[-1])
        )

    def emit(self: gate) -> str:
        """
        Emit a Bristol Fashion string for this gate.
        """
        return " ".join([
            str(self.wire_in_count), str(self.wire_out_count),
            " ".join([str(i) for i in self.wire_in_index]),
            " ".join([str(i) for i in self.wire_out_index]),
            self.operation.emit()
        ])

class bfc():
    """
    Data structure for circuits represented using the Bristol Fashion.
    A string representing a circuit that conforms to the Bristol Fashion
    syntax can be parsed into an instance of this class.

    >>> circuit_string = ['7 36', '2 4 4', '1 1']
    >>> circuit_string.extend(['2 1 0 1 15 AND', '2 1 2 3 16 AND'])
    >>> circuit_string.extend(['2 1 15 16 8 AND', '2 1 4 5 22 AND'])
    >>> circuit_string.extend(['2 1 6 7 23 AND', '2 1 22 23 9 AND'])
    >>> circuit_string.extend(['2 1 8 9 35 AND'])
    >>> circuit_string = "\\n".join(circuit_string)
    >>> c = bfc(circuit_string)

    The string representation can be recovered from an instance of this
    class, as well.

    >>> c.emit() == circuit_string
    True
    >>> for line in c.emit().split("\\n"):
    ...     print(line)
    7 36
    2 4 4
    1 1
    2 1 0 1 15 AND
    2 1 2 3 16 AND
    2 1 15 16 8 AND
    2 1 4 5 22 AND
    2 1 6 7 23 AND
    2 1 22 23 9 AND
    2 1 8 9 35 AND

    A circuit can also be consructed using an instance of the
    :obj:`~circuit.circuit.circuit` class defined in the
    `circuit <https://pypi.org/project/circuit/>`_ library (see the
    documentation for the :obj:`circuit.circuit` method defined as part of
    this class).

    Common properties of the circuit can be found in the attributes of
    an instance.

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

    The individual gates are stored within a list consisting of zero or
    more instances of the :obj:`gate` class.

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

    A circuit can also be evaluated an on a sequence of input bit vectors
    using the :obj:`bfcl.evaluate` method.

    >>> from itertools import product
    >>> inputs = list(product(*([[0, 1]]*4)))
    >>> pairs = product(inputs, inputs)
    >>> outputs = ([0]*255) + [1]
    >>> [c.evaluate(p)[0][0] for p in pairs] == outputs
    True
    """
    def __init__(self: bfc, raw=None):
        """Initialize a bfc data structure instance."""
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

    def circuit(self: bfc, c: circuit_.circuit=None) -> Union[Type[None], circuit_.circuit]:
        """
        Populate this Bristol Fashion circuit instance using an instance of the
        :obj:`~circuit.circuit.circuit` class defined in the
        `circuit <https://pypi.org/project/circuit/>`_ library.

        >>> c_ = circuit_.circuit()
        >>> c_.count()
        0
        >>> g0 = c_.gate(op.id_, is_input=True)
        >>> g1 = c_.gate(op.id_, is_input=True)
        >>> g2 = c_.gate(op.and_, [g0, g1])
        >>> g3 = c_.gate(op.id_, [g2], is_output=True)
        >>> c_.count()
        4
        >>> c = bfc(c_)
        >>> c.emit().split("\\n")
        ['2 4', '1 2', '1 1', '2 1 0 1 2 AND', '1 1 2 3 LID']
        >>> c_reparsed = bfc(bfc(c_).circuit())
        >>> c_reparsed.emit().split("\\n")
        ['2 4', '1 2', '1 1', '2 1 0 1 2 AND', '1 1 2 3 LID']
        """
        if c:
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
            for g in c.gate:
                if len(g.inputs) > 0:
                    self.gate.append(gate(
                        len(g.inputs), 1,
                        [ig.index for ig in g.inputs], [g.index],
                        operation(g.operation)
                    ))
            return None
        #else if (c == None):
        input_format = self.value_in_length
        output_format = self.value_out_length
        c = circuit_.circuit(circuit_.signature(input_format, output_format))

        if not (
                all(self.gate[gate_index].operation == circuit_.op.id_ for gate_index in
                                            range(self.gate_count - self.wire_out_count, self.gate_count)) and
                self.wire_out_index == list(range(self.wire_count - self.wire_out_count, self.wire_count))
        ):
            #raise NotImplementedError("The bfcl library only supports converting to a circuit object for circuits"
            #                          " with in-order identity-gate outputs.")
            # Update circuit to new output format.
            self.gate.extend(
                [
                    gate(
                        1,
                        1,
                        [i - self.wire_out_count],
                        [i],
                        operation(circuit_.op.id_)  # operation.parse('LID')
                    )
                    for i in range(self.wire_count, self.wire_count + self.wire_out_count)
                ]
            )



        intermediate_gates = self.gate[:]
        output_gates = self.gate[-self.wire_out_count:]
        wires = []
        for _g in range(self.wire_in_count):#input_gates:
            wires.append(
                c.gate(
                    circuit_.op.id_,
                    is_input=True
                )
            )
        wires.extend([None] * len(intermediate_gates))
        for g in intermediate_gates:
            assert(len(g.wire_in_index) > 0)
            assert(len(g.wire_out_index) > 0)
            _g = c.gate(
                g.operation,
                list(map(lambda i : wires[i], g.wire_in_index))
            )
            for wire_out_index in g.wire_out_index:
                assert(wire_out_index > self.wire_in_count - 1)  # Assert well ordering of inputs gates (to wires).
                wires[wire_out_index] = _g
        for g in output_gates:
            assert(len(g.wire_in_index) > 0)
            c.gate(
                g.operation,  # This should always be `circuit_.op.id_`.
                list(map(lambda i : wires[i], g.wire_in_index)),
                is_output=True
            )
        c.prune_and_topological_sort_stable()

        return c

    def parse(self: circuit, raw: str):
        """
        Parse a string representation of a circuit that conforms to the Bristol
        Fashion syntax.

        >>> s = ['7 36', '2 4 4', '1 1']
        >>> s.extend(['2 1 0 1 15 AND', '2 1 2 3 16 AND'])
        >>> s.extend(['2 1 15 16 8 AND', '2 1 4 5 22 AND'])
        >>> s.extend(['2 1 6 7 23 AND', '2 1 22 23 9 AND'])
        >>> s.extend(['2 1 8 9 35 AND'])
        >>> s = "\\n".join(s)
        >>> c = bfc()
        >>> c.parse(s)
        >>> for line in c.emit().split("\\n"):
        ...     print(line)
        7 36
        2 4 4
        1 1
        2 1 0 1 15 AND
        2 1 2 3 16 AND
        2 1 15 16 8 AND
        2 1 4 5 22 AND
        2 1 6 7 23 AND
        2 1 22 23 9 AND
        2 1 8 9 35 AND
        """
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

    def emit(self: circuit, force_id_outputs=False, progress=lambda _: _) -> str:
        """
        Emit a string representation of a Bristol Fashion circuit definition.

        In the example below, a circuit object is first constructed using the
        `circuit <https://pypi.org/project/circuit/>`_ library.

        >>> c_ = circuit_.circuit()
        >>> c_.count()
        0
        >>> g0 = c_.gate(op.id_, is_input=True)
        >>> g1 = c_.gate(op.id_, is_input=True)
        >>> g2 = c_.gate(op.and_, [g0, g1])
        >>> g3 = c_.gate(op.id_, [g2], is_output=True)

        The ``c_`` object above can be converted into an instance of the
        class :obj:`circuit`.

        >>> c = bfc(c_)

        This method can be used to emit a string representation of an object,
        where the string conforms to the Bristol Fashion syntax.

        >>> c.emit().split("\\n")
        ['2 4', '1 2', '1 1', '2 1 0 1 2 AND', '1 1 2 3 LID']

        >>> c.emit(True).split("\\n")
        ['2 4', '1 2', '1 1', '2 1 0 1 2 AND', '1 1 2 3 LID']
        """
        _self = bfc(self.circuit()) if force_id_outputs else self  # Temporarily post-process if flag is True.
        lines = [
            [str(_self.gate_count), str(_self.wire_count)],
            [str(_self.value_in_count)] + list(map(str, _self.value_in_length)),
            [str(_self.value_out_count)] + list(map(str, _self.value_out_length))
        ]
        lines.extend([[g.emit()] for g in progress(_self.gate)])
        return "\n".join(" ".join(line) for line in lines)

    def evaluate(
            self: circuit,
            inputs: Sequence[Sequence[int]]
        ) -> Sequence[Sequence[int]]:
        """
        Evaluate a circuit on a sequence of input bit vectors.

        >>> s = ['7 36', '2 4 4', '1 1']
        >>> s.extend(['2 1 0 1 15 AND', '2 1 2 3 16 AND'])
        >>> s.extend(['2 1 15 16 8 AND', '2 1 4 5 22 AND'])
        >>> s.extend(['2 1 6 7 23 AND', '2 1 22 23 9 AND'])
        >>> s.extend(['2 1 8 9 35 AND'])
        >>> c = bfc("\\n".join(s))
        >>> c.evaluate([[1, 0, 1, 1], [1, 1, 1, 0]])
        [[0]]
        >>> c.evaluate([[1, 1, 1, 1], [1, 1, 1, 1]])
        [[1]]

        The example below confirms that the circuit ``c`` defined above has correct
        behavior when evaluated on all compatible inputs (*i.e.*, inputs consisting
        of a pair of 4-bit vectors).

        >>> from itertools import product
        >>> inputs = list(product(*([[0, 1]]*4)))
        >>> pairs = product(inputs, inputs)
        >>> outputs = ([0]*255) + [1]
        >>> [c.evaluate(p)[0][0] for p in pairs] == outputs
        True
        """
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
    doctest.testmod() # pragma: no cover
