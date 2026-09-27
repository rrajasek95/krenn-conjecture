#!/usr/bin/env python3
"""Independent seven-site determinant check (requires python-flint).

Run with the repository's .venv/bin/python. Does not write any files.
The C certificate uses Pfaffian elimination; this uses FLINT's determinant.
"""

import json

from flint import nmod_mat
from verify import dense, exterior_sparse, words


def main():
    ws = words(7)
    state = 1729
    tensor = []
    for w in ws:
        state = (state ^ (state << 13)) & 0xFFFFFFFF
        state = (state ^ (state >> 17)) & 0xFFFFFFFF
        state = (state ^ (state << 5)) & 0xFFFFFFFF
        tensor.append(1 + state % 100 if 0 in w else 0)
    matrix = dense(exterior_sparse(tensor, ws, 101))
    assert all(row[0] == 0 for row in matrix)
    assert all(sum(x * y for x, y in zip(row, tensor)) % 101 == 0 for row in matrix)
    minor = nmod_mat([row[3:] for row in matrix[3:]], 101)
    determinant = int(minor.det())
    assert determinant == 22 == 27**2 % 101
    print(json.dumps({
        "implementation": "python-flint nmod_mat.det",
        "minor_order": 2184,
        "prime": 101,
        "determinant": determinant,
        "agrees_with_C_pfaffian_square": True,
        "product_vector_in_kernel": True,
        "tensor_in_kernel": True,
    }, indent=2))


if __name__ == "__main__":
    main()
