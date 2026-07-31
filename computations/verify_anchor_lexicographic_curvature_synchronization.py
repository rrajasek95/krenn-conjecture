#!/usr/bin/env python3
"""Light exact audit of anchor-first curvature synchronization.

The proof is uniform.  This checker audits the two new finite incidence
lemmas: a pure-port merge can preserve every mutual coordinate anchor, and
the scalar-unit row deletion cannot remove one.  It is dependency-free and
uses explicit failures so that ``python -O`` changes nothing.
"""

from fractions import Fraction


F = Fraction
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def support(cells):
    return {key for key, value in cells.items() if value}


def degrees(cells):
    answer = {}
    for (left, left_colour, right, right_colour), value in cells.items():
        if not value:
            continue
        u = (left, left_colour)
        v = (right, right_colour)
        answer[u] = answer.get(u, 0) + 1
        answer[v] = answer.get(v, 0) + 1
    return answer


def anchors(cells):
    degree = degrees(cells)
    return {
        key
        for key in support(cells)
        if degree[(key[0], key[1])] == degree[(key[2], key[3])] == 1
    }


def add_cell(cells, left, left_colour, right, right_colour, value):
    require(left < right, "cells must use the fixed physical order")
    key = (left, left_colour, right, right_colour)
    cells[key] = cells.get(key, F(0)) + F(value)


def pure_port_packet():
    """A three-fibre star with anchored and cancelling split ports."""
    cells = {}
    # Centre 0.  Fibre 0 has an anchored diagonal representative plus a
    # cancelling transverse pair.  The other fibres have one port each.
    ports = {
        1: (0, (1, 0, 0)),
        2: (0, (0, 1, 0)),
        3: (0, (0, -1, 0)),
        4: (1, (0, 1, 0)),
        5: (2, (0, 0, 1)),
    }
    for site, (fibre, vector) in ports.items():
        for centre_colour, value in enumerate(vector):
            if value:
                add_cell(cells, 0, centre_colour, site, fibre, value)

    # Old anchors away from the centre, including one at a representative
    # site in a coordinate different from its port coordinate.
    add_cell(cells, 2, 2, 6, 2, 7)
    add_cell(cells, 5, 0, 7, 0, 11)
    return cells, ports


def fibre_sums(ports):
    sums = [[F(0) for _ in COLOURS] for _ in COLOURS]
    for _site, (fibre, vector) in ports.items():
        for coordinate, value in enumerate(vector):
            sums[fibre][coordinate] += F(value)
    return sums


def choose_anchor_preserving_representatives(cells, ports):
    old_anchors = anchors(cells)
    chosen = {}
    for fibre in COLOURS:
        candidates = [site for site, data in ports.items() if data[0] == fibre]
        require(candidates, "empty pure-port fibre")
        anchored = [
            site
            for site in candidates
            if (0, fibre, site, fibre) in old_anchors
        ]
        require(len(anchored) <= 1, "two anchored ports in one fibre")
        chosen[fibre] = anchored[0] if anchored else candidates[0]
    return chosen


def merge_ports(cells, ports, chosen):
    merged = {
        key: value
        for key, value in cells.items()
        if key[0] != 0 and key[2] != 0
    }
    for fibre, site in chosen.items():
        add_cell(merged, 0, fibre, site, fibre, 1)
    return merged


def audit_port_merge():
    cells, ports = pure_port_packet()
    require(
        fibre_sums(ports)
        == [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]],
        "pure-port fibres do not sum to the target basis",
    )
    old_anchors = anchors(cells)
    chosen = choose_anchor_preserving_representatives(cells, ports)
    merged = merge_ports(cells, ports, chosen)
    require(old_anchors <= anchors(merged), "port merge destroyed an old anchor")
    old_star = {key for key in support(cells) if key[0] == 0 or key[2] == 0}
    new_star = {key for key in support(merged) if key[0] == 0 or key[2] == 0}
    require(len(new_star) == 3, "merged star is not cubic")
    require(len(old_star) > len(new_star), "noncubic merge did not lower support")

    # Choosing site 2 instead of the anchored site 1 in fibre zero deletes
    # the old centre anchor.  The prescribed choice must detect this.
    wrong = dict(chosen)
    wrong[0] = 2
    require(
        not old_anchors <= anchors(merge_ports(cells, ports, wrong)),
        "wrong representative mutation did not destroy the planted anchor",
    )

    # Inserting at a coordinate which had no old port can destroy an
    # unrelated anchor; the pure endpoint coordinate is essential.
    bad = merge_ports(cells, ports, chosen)
    add_cell(bad, 2, 2, 6, 1, 1)
    require(
        not old_anchors <= anchors(bad),
        "free-coordinate insertion mutation escaped detection",
    )


def scalar_unit_packet():
    cells = {}
    # Direct aa cell and a nonzero selected residual row make (p,a)
    # non-anchored.  Complementary rows contain two genuine anchors.
    add_cell(cells, 0, 0, 1, 0, 3)
    add_cell(cells, 0, 0, 2, 1, 5)
    add_cell(cells, 0, 1, 3, 1, 7)
    add_cell(cells, 0, 2, 4, 2, 11)
    add_cell(cells, 2, 0, 5, 0, 13)
    add_cell(cells, 3, 2, 6, 2, 17)
    return cells


def delete_selected_residual_row(cells, site=0, partner=1, selected=0):
    """Delete the selected off-pair star row, retaining the direct block."""
    return {
        key: value
        for key, value in cells.items()
        if not (
            (
                (key[0] == site and key[1] == selected)
                or (key[2] == site and key[3] == selected)
            )
            and {key[0], key[2]} != {site, partner}
        )
    }


def audit_row_deletion():
    cells = scalar_unit_packet()
    old_anchors = anchors(cells)
    deleted = delete_selected_residual_row(cells)
    require(old_anchors <= anchors(deleted), "selected-row deletion lost an anchor")
    require(len(support(deleted)) < len(support(cells)), "row deletion was not strict")
    require(
        deleted[(0, 0, 1, 0)] == cells[(0, 0, 1, 0)],
        "selected-row deletion changed the direct scalar cell",
    )
    require(
        (0, 0, 2, 1) not in support(deleted),
        "selected residual star row was not deleted",
    )
    require(
        all(not (key[0] == 0 and key[1] == 0) for key in old_anchors),
        "selected coordinate was incorrectly counted as an old anchor",
    )

    # Without the direct scalar cell, the selected star cell can itself be
    # an anchor and deletion can destroy it.  This checks the scalar-unit
    # hypothesis used by the proof.
    mutated = dict(cells)
    mutated[(0, 0, 1, 0)] = F(0)
    planted = anchors(mutated)
    require(
        not planted <= anchors(delete_selected_residual_row(mutated)),
        "missing-direct-cell mutation escaped detection",
    )


def main():
    audit_port_merge()
    audit_row_deletion()
    print("anchor-first curvature synchronization: PASS")
    print("pure-port merge and scalar-unit deletion preserve all old anchors")


if __name__ == "__main__":
    main()
