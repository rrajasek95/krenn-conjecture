#!/usr/bin/env python3
"""Non-minimal pair/triple guard at the corrected 18-cell minimum.

The variables are the 38 balanced elementary two-cell rays which are
port-Gram orthogonal to the current support.  A multi-ray support is retained
only when its union is still port-Gram orthogonal and has literal blockers for
all 728 arbitrary-K carriers.  Gaussian phases are exact for the real
coefficient quadratic form; amplitudes are then minimized by principal
minors/eigenvectors rather than being fixed equal.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import integrate_global_normal_counterfamily as current  # noqa: E402
import screen_next_active_set_descent as single  # noqa: E402
from probe_laurent_crosscolour_leakage import enumerate_feasible  # noqa: E402


PHASES = (1, -1, 1j, -1j)
VMID = sum(single.VBOX if hasattr(single, "VBOX") else (single.VLO, single.VHI)) / 2
WMID = sum(single.WBOX if hasattr(single, "WBOX") else (single.WLO, single.WHI)) / 2


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def gram_orthogonal(support):
    remote = defaultdict(set)
    for u, v, a, b in support:
        remote[u, v, b].add(a)
        remote[v, u, a].add(b)
    return all(len(colours) == 1 for colours in remote.values())


def full_blocker(indices, rays):
    source = {cell: None for cell in single.CURRENT_SUPPORT}
    for index in indices:
        source.update({cell: None for cell in rays[index]})
    try:
        stars, triangles = family.carrier_witnesses(source)
    except RuntimeError:
        return False
    return len(stars) == 168 and len(triangles) == 560


def term_ledger(active_cells):
    support = single.CURRENT_SUPPORT | set(active_cells)
    edge_cells = defaultdict(list)
    for cell in support:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


RAW_SOURCE = current.source_box(WMID, WMID, VMID, VMID)
BASE_SOURCE = {cell: (value.lo + value.hi) / 2
               for cell, (value, _) in RAW_SOURCE.items()}


def q_complex(direction, ledger):
    degree = defaultdict(float)
    for (u, v, a, b), value in direction.items():
        square = abs(value) ** 2
        degree[u, a] += square
        degree[v, b] += square
    source_z = {}
    for colour, layer in family.LAYERS.items():
        gaps = [BASE_SOURCE[edge + (colour, colour)] ** 2 for edge in layer]
        values = []
        for u, v in layer:
            require(abs(degree[u, colour] - degree[v, colour]) < 1e-10,
                    (direction, colour, u, v, degree))
            values.append(degree[u, colour])
        rho_z = sum(value / gap for value, gap in zip(values, gaps))
        rho_z /= sum(1 / gap for gap in gaps)
        for edge, value in zip(layer, values):
            diagonal = BASE_SOURCE[edge + (colour, colour)]
            source_z[edge + (colour, colour)] = (rho_z - value) / (2 * diagonal)
    for cell in current.BOUNDARY:
        source_z[cell] = 0.0
    for cell in current.DIRECTION:
        source_z[cell] = 0.0

    q = 0.0
    for word, monomials in ledger.items():
        if len(set(word)) == 1:
            continue
        f0 = 0j
        linear = 0j
        quadratic = 0j
        for monomial in monomials:
            count = sum(cell in direction for cell in monomial)
            if count == 0:
                value = 1.0
                for cell in monomial:
                    value *= BASE_SOURCE[cell]
                f0 += value
                derivative = 0.0
                for index, cell in enumerate(monomial):
                    piece = source_z[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece *= BASE_SOURCE[other_cell]
                    derivative += piece
                quadratic += derivative
            elif count in (1, 2):
                value = 1 + 0j
                for cell in monomial:
                    value *= direction[cell] if cell in direction else BASE_SOURCE[cell]
                if count == 1:
                    linear += value
                else:
                    quadratic += value
        q += abs(linear) ** 2 + 2 * (f0.conjugate() * quadratic).real
    return q


def phase_states(ray):
    return tuple({ray[0]: left, ray[1]: right}
                 for left, right in product(PHASES, repeat=2))


def add_directions(left, right):
    answer = dict(left)
    for cell, value in right.items():
        answer[cell] = answer.get(cell, 0) + value
    return {cell: value for cell, value in answer.items() if value}


def det2(a, b, cross):
    return a * b - cross * cross


def main():
    all_rays = sorted({tuple(sorted(row["cells"])) for row in enumerate_feasible()})
    rays = [ray for ray in all_rays if not set(ray) & single.CURRENT_SUPPORT
            and gram_orthogonal(single.CURRENT_SUPPORT | set(ray))]
    require(len(rays) == 38, len(rays))
    singleton_full = [i for i in range(38) if full_blocker((i,), rays)]
    pairs = []
    for i, j in combinations(range(38), 2):
        support = single.CURRENT_SUPPORT | set(rays[i]) | set(rays[j])
        if gram_orthogonal(support) and full_blocker((i, j), rays):
            pairs.append((i, j))
    print("rays", len(rays), "singleton full", len(singleton_full),
          "Gram/full pairs", len(pairs))

    singleton_ledgers = {i: term_ledger(rays[i]) for i in range(38)}
    pair_ledgers = {(i, j): term_ledger(rays[i] + rays[j]) for i, j in pairs}
    diagonal = {}
    for i in range(38):
        states = phase_states(rays[i])
        for si, state in enumerate(states):
            diagonal[i, si] = q_complex(state, singleton_ledgers[i])

    best = None
    tested = 0
    for i, j in pairs:
        states_i, states_j = phase_states(rays[i]), phase_states(rays[j])
        for si, sj in product(range(16), repeat=2):
            a, b = diagonal[i, si], diagonal[j, sj]
            total = q_complex(add_directions(states_i[si], states_j[sj]),
                              pair_ledgers[i, j])
            cross = (total - a - b) / 2
            determinant = det2(a, b, cross)
            tested += 1
            record = (determinant, a, b, cross, i, j, si, sj)
            if best is None or record < best:
                best = record
            if determinant < -1e-9 or a < -1e-9 or b < -1e-9:
                print("NEGATIVE_PAIR", record)
                print("ray i", rays[i], "state", states_i[si])
                print("ray j", rays[j], "state", states_j[sj])
                print("support full", full_blocker((i, j), rays),
                      "Gram", gram_orthogonal(single.CURRENT_SUPPORT
                                               | set(rays[i]) | set(rays[j])))
                return
    print("phase pair states", tested, "best determinant", best)
    require(best is not None, "no pairs")


if __name__ == "__main__":
    main()
