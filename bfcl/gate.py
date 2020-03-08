"""Circuit data structure.

Python library for working with circuit definitions
represented using the Bristol Fashion.
"""

import doctest

class Gate():
    """
    Class for circuit gates.
    """

    def __init__(\
            self,
            wire_in_count = None, wire_out_count = None,
            wire_in_index = [], wire_out_index = [],
            operation = None
        ):
        """Initialize a gate data structure instance."""
        self.wire_in_count = wire_in_count
        self.wire_out_count = wire_out_count
        self.wire_in_index = wire_in_index
        self.wire_out_index = wire_out_index
        self.operation = operation

    @staticmethod
    def operation_from_bristol_fashion_string(raw):
        """Parse a Bristol Fashion circuit gate operator string."""
        convert = {'AND':'AND', 'XOR':'XOR', 'INV':'NOT'}
        return convert[raw.upper().strip()]

if __name__ == "__main__":
    doctest.testmod()
