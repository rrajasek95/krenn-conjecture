#!/usr/bin/env python3
"""Exact audit of the 32-cell frontier for mixed-endpoint coordinate q.

This checker freezes only the theorem boundary proved by the support search:
for one-site coordinate response rows, every exact mixed-endpoint coordinate
solution needs at least 32 active aggregate q cells.  It does not claim that
the support relaxation is sufficient above that boundary.
"""

from __future__ import annotations

from itertools import product

from search_mixed_endpoint_one_site_support import (
    ROW_GEOMETRIES,
    SupportSystem,
    audit_minimum_layer,
    audit_path_edge_31_layer,
)
from verify_sparse_nonpure_coordinate_response_obstructions import (
    COLOURS,
    ROW_ORBITS,
    edge,
)


WORDS4 = tuple(product(COLOURS, repeat=4))


def has_direct_block_conflict(rows):
    """Test whether diagonal and off-diagonal equations sample one block
    with incompatible target/zero requirements.

    This filter is independent of q.  A repeated requirement with the same
    truth value is harmless; a target coefficient also required to vanish is
    an immediate contradiction.
    """

    requirements = {}

    def insert(pair, word, target):
        key = pair, word
        old = requirements.get(key)
        if old is not None and old != target:
            return True
        requirements[key] = target
        return False

    for i, (a, b) in enumerate(rows):
        pair = edge(a, b)
        for word in WORDS4:
            if insert(pair, word, word == (i,) * 4):
                return True

        for j in COLOURS:
            if i == j:
                continue
            p_site = rows[i][0]
            s_site = rows[j][1]
            if p_site == s_site:
                continue
            pair = edge(p_site, s_site)
            for word in WORDS4:
                if insert(pair, word, False):
                    return True
    return False


def audit_row_block_filter():
    survivors = tuple(
        rows for rows in ROW_ORBITS if not has_direct_block_conflict(rows)
    )
    assert survivors == tuple(ROW_GEOMETRIES.values())
    return survivors


def main():
    survivors = audit_row_block_filter()
    print("direct row-block-compatible one-site orbits:", survivors)

    path_system = SupportSystem(ROW_GEOMETRIES["path-edge"])
    path_minimum = audit_minimum_layer("path-edge", path_system)
    path_31 = audit_path_edge_31_layer(path_system)
    assert path_minimum[1] == 31
    assert path_31[1] == 32
    print("path-edge minimum-layer audit:", path_minimum)
    print("path-edge 31-cell-layer audit:", path_31)

    matching_system = SupportSystem(ROW_GEOMETRIES["matching"])
    matching_minimum = audit_minimum_layer("matching", matching_system)
    assert matching_minimum[1] == 32
    print("matching minimum-layer audit:", matching_minimum)

    print("mixed-endpoint one-site exact solutions need >=32 active cells: PASS")


if __name__ == "__main__":
    main()
