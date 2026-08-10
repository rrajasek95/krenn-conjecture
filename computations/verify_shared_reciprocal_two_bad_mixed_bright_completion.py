#!/usr/bin/env python3
"""Exact first mixed-cell bright completion and nonlinear boundary.

The canonical first parity transgression on five sites is

    12:aa, 34:cc, 02:ta,
    U = e_t@0 - e_a@1 in ker(Phi).

This checker classifies the direct two-cell completion by pure matching
leaders.  Up to 3<->4 it is 01:cc, 03:aa; it contains both bright pure
classes, still excludes X_t, and forces the unused cofactor K_3 to vanish.

The only one-cell activation of K_3 which preserves the same bridge and
both bright classes is 04:rs.  All nine endpoint-colour choices are checked
over Q.  Even 04:tt does not put X_t in im(Phi) plus the complete linear
span of P*U*V*q for U,V in ker(Phi).

This is a bounded exact chart theorem, not the full mixed-colour theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json

import sympy as sp


SITES = tuple(range(5))
A, C, T = range(3)
WORDS = tuple(itertools.product(range(3), repeat=5))
LABELS = tuple(itertools.product(SITES, range(3)))
EXPECTED_DIGEST = "f80a767fcdcb7e0bebeee6d57330693d5e3556176f44586e45b993c4f1ac6958"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def put(cells, u, v, left, right, value=1):
    if u > v:
        u, v, left, right = v, u, right, left
    cells[((u, v), left, right)] = sp.sympify(value)


def matching_tensor(vertices, cells):
    vertices = tuple(vertices)
    answer = defaultdict(lambda: sp.S.Zero)
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            entries = [
                (left, right, value)
                for (candidate, left, right), value in cells.items()
                if candidate == edge and value != 0
            ]
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in itertools.product(*choices):
                colouring = {}
                coefficient = sp.S.One
                for edge, (left, right, value) in zip(matching, selected):
                    colouring[edge[0]] = left
                    colouring[edge[1]] = right
                    coefficient *= value
                answer[tuple(colouring[site] for site in vertices)] += coefficient
    return {word: sp.simplify(value) for word, value in answer.items()
            if value != 0}


def insert(cofactor, sites, hole, colour):
    answer = {}
    for word, value in cofactor.items():
        colouring = dict(zip(sites, word))
        colouring[hole] = colour
        answer[tuple(colouring[site] for site in SITES)] = value
    return answer


def phi_matrix(cells):
    columns = []
    cofactors = {}
    for hole in SITES:
        sites = tuple(site for site in SITES if site != hole)
        cofactors[hole] = matching_tensor(sites, cells)
        for colour in range(3):
            tensor = insert(cofactors[hole], sites, hole, colour)
            columns.append(sp.Matrix([tensor.get(word, 0) for word in WORDS]))
    return sp.Matrix.hstack(*columns), cofactors


def vector_as_rows(vector):
    rows = {}
    for index, value in enumerate(vector):
        if value:
            site, colour = LABELS[index]
            rows.setdefault(site, {})[colour] = value
    return rows


def kernel_product(cells, p_rows, u_rows, v_rows):
    tensor = defaultdict(lambda: sp.S.Zero)
    for x, pvector in p_rows.items():
        for y, uvector in u_rows.items():
            for z, vvector in v_rows.items():
                if len({x, y, z}) < 3:
                    continue
                edge = tuple(sorted(set(SITES) - {x, y, z}))
                for (candidate, left, right), edge_value in cells.items():
                    if candidate != edge:
                        continue
                    for px, pv in pvector.items():
                        for uy, uv in uvector.items():
                            for vz, vv in vvector.items():
                                colours = {
                                    x: px, y: uy, z: vz,
                                    edge[0]: left, edge[1]: right,
                                }
                                word = tuple(colours[site] for site in SITES)
                                tensor[word] += pv * uv * vv * edge_value
    return sp.Matrix([sp.simplify(tensor[word]) for word in WORDS])


def in_span(matrix, vector):
    return matrix.rank() == matrix.row_join(vector).rank()


def full_audit(cells):
    phi, cofactors = phi_matrix(cells)
    pure = {
        colour: sp.Matrix([int(word == (colour,) * 5) for word in WORDS])
        for colour in range(3)
    }
    kernel = phi.nullspace()
    products = []
    for p_index in range(len(LABELS)):
        p = sp.zeros(len(LABELS), 1)
        p[p_index] = 1
        for u in kernel:
            for v in kernel:
                products.append(kernel_product(
                    cells, vector_as_rows(p), vector_as_rows(u),
                    vector_as_rows(v)))
    augmented = phi if not products else phi.row_join(sp.Matrix.hstack(*products))
    pure_matrix = sp.Matrix.hstack(*(pure[colour] for colour in range(3)))
    pure_intersection = (
        augmented.rank() + 3 - augmented.row_join(pure_matrix).rank()
    )
    return {
        "phi": phi,
        "cofactors": cofactors,
        "kernel": kernel,
        "pure": pure,
        "augmented": augmented,
        "summary": (
            phi.rank(), len(kernel), augmented.rank(), pure_intersection,
            tuple(in_span(phi, pure[colour]) for colour in range(3)),
            in_span(augmented, pure[T]),
        ),
    }


def cell_character_rank(cells):
    half_edges = tuple(itertools.product(SITES, range(3)))
    columns = []
    for (edge, left, right) in cells:
        column = sp.zeros(len(half_edges), 1)
        column[half_edges.index((edge[0], left))] = 1
        column[half_edges.index((edge[1], right))] = 1
        columns.append(column)
    return sp.Matrix.hstack(*columns).rank()


def base_cells():
    cells = {}
    put(cells, 1, 2, A, A)
    put(cells, 3, 4, C, C)
    put(cells, 0, 2, T, A)
    return cells


def bridge_support(cells):
    phi, _ = phi_matrix(cells)
    left = {WORDS[index] for index, value in enumerate(phi[:, LABELS.index((0, T))])
            if value}
    right = {WORDS[index] for index, value in enumerate(phi[:, LABELS.index((1, A))])
             if value}
    return left, right


def classify_direct_completion():
    # A direct X_a lift completes 12:aa by one aa edge on the other three
    # sites.  A direct X_c lift similarly completes 34:cc.
    a_edges = ((0, 3), (0, 4), (3, 4))
    c_edges = ((0, 1), (0, 2), (1, 2))
    cases = []
    for a_edge, c_edge in itertools.product(a_edges, c_edges):
        cells = base_cells()
        put(cells, *a_edge, A, A)
        put(cells, *c_edge, C, C)
        left, right = bridge_support(cells)
        if left == right and len(left) == 1:
            audit = full_audit(cells)
            cases.append({
                "a_edge": a_edge,
                "c_edge": c_edge,
                "dead_holes": tuple(hole for hole, tensor
                                    in audit["cofactors"].items() if not tensor),
                "summary": audit["summary"],
            })
    require(len(cases) == 2, "direct bright-completion orbit changed")
    require({case["a_edge"] for case in cases} == {(0, 3), (0, 4)},
            "direct a-completion edges changed")
    require({case["c_edge"] for case in cases} == {(0, 1)},
            "direct c-completion edge changed")
    require({case["dead_holes"] for case in cases} == {(3,), (4,)},
            "minimal completion no longer forces a dead cofactor")
    return cases


def representative_cells(extra=None):
    cells = base_cells()
    put(cells, 0, 1, C, C)
    put(cells, 0, 3, A, A)
    if extra is not None:
        left, right = extra
        put(cells, 0, 4, left, right)
    return cells


def audit_one_cell_activation():
    valid = []
    all_cells = tuple(
        (edge, left, right)
        for edge in itertools.combinations(SITES, 2)
        for left in range(3) for right in range(3)
    )
    base = representative_cells()
    for key in all_cells:
        if key in base:
            continue
        cells = dict(base)
        cells[key] = sp.S.One
        left, right = bridge_support(cells)
        if left != right or len(left) != 1:
            continue
        audit = full_audit(cells)
        images = audit["summary"][4]
        if images[:2] != (True, True) or images[2]:
            continue
        if all(audit["cofactors"].values()):
            valid.append((key, audit["summary"], cell_character_rank(cells)))

    require(len(valid) == 9, "one-cell activation census changed")
    require({key[0] for key, _, _ in valid} == {(0, 4)},
            "an unexpected physical activation survived")
    require({(key[1], key[2]) for key, _, _ in valid}
            == set(itertools.product(range(3), repeat=2)),
            "not all endpoint colours survived on 04")
    require(all(rank == 6 for _, _, rank in valid),
            "one-cell chart lost independent torus normalization")
    require(all(not summary[-1] for _, summary, _ in valid),
            "a one-cell activation acquired the nonlinear pure class")
    return valid


def audit_full_04_block():
    """Allow an arbitrary endpoint-colour matrix on physical edge 04.

    The tt entry is a nonzero parameter z.  Its three word coordinates give
    private pivots for the three hole-3 columns, so the full cofactor map has
    rank 14 for every specialization of the other eight entries.  The one
    remaining kernel is the original tilted bridge.
    """
    cells = representative_cells()
    z = sp.Symbol("z", nonzero=True)
    parameters = {}
    for left, right in itertools.product(range(3), repeat=2):
        value = z if (left, right) == (T, T) else sp.Symbol(
            f"b{left}{right}")
        parameters[(left, right)] = value
        put(cells, 0, 4, left, right, value)

    phi, cofactors = phi_matrix(cells)
    bridge = sp.zeros(len(LABELS), 1)
    bridge[LABELS.index((0, T))] = 1
    bridge[LABELS.index((1, A))] = -1
    require(phi * bridge == sp.zeros(len(WORDS), 1),
            "the full 04 block broke the tilted bridge")

    old_labels = [
        label for label in LABELS
        if label[0] in (0, 1, 2, 4) and label != (1, A)
    ]
    old_rows = []
    for label in old_labels:
        column = phi[:, LABELS.index(label)]
        support = [index for index, value in enumerate(column) if value]
        require(len(support) == 1,
                "an old direct column ceased to be a monomial")
        old_rows.append(support[0])
    require(len(set(old_rows)) == 11,
            "the eleven old pivot words ceased to be distinct")

    private_words = [(T, A, A, colour, T) for colour in range(3)]
    private_rows = [WORDS.index(word) for word in private_words]
    selected_labels = old_labels + [(3, colour) for colour in range(3)]
    selected_rows = old_rows + private_rows
    minor = phi.extract(
        selected_rows, [LABELS.index(label) for label in selected_labels]
    )
    determinant = sp.factor(minor.det())
    require(determinant in (z ** 3, -z ** 3),
            f"the full-block private pivot changed: {determinant}")

    # The explicit relation gives rank <=14, while the minor gives rank >=14.
    # Hence ker(Phi)=<bridge>.  It remains to inspect only P*bridge^2*q.
    target_index = WORDS.index((T,) * 5)
    require(all(phi[target_index, column] == 0
                for column in range(phi.cols)),
            "the full 04 block acquired X_t in im(Phi)")
    product_target_coefficients = []
    for p_index in range(len(LABELS)):
        p = sp.zeros(len(LABELS), 1)
        p[p_index] = 1
        product = kernel_product(
            cells, vector_as_rows(p), vector_as_rows(bridge),
            vector_as_rows(bridge))
        product_target_coefficients.append(
            sp.factor(product[target_index])
        )
    require(product_target_coefficients == [0] * len(LABELS),
            "the full 04 block acquired a pure tilted-kernel product")

    pure_a = sp.Matrix([int(word == (A,) * 5) for word in WORDS])
    pure_c = sp.Matrix([int(word == (C,) * 5) for word in WORDS])
    require(in_span(phi, pure_a) and in_span(phi, pure_c),
            "the full 04 block lost a bright pure class")
    require(all(cofactors.values()),
            "the nonzero tt entry failed to activate every cofactor")
    return {
        "free_entries": 8,
        "nonzero_entry": "b22=z",
        "pivot_determinant": str(determinant),
        "rank": 14,
        "kernel_dimension": 1,
        "zero_kernel_product_target_coefficients": len(
            product_target_coefficients
        ),
    }


def main():
    direct = classify_direct_completion()
    representative = full_audit(representative_cells())
    require(representative["summary"]
            == (11, 4, 13, 2, (True, True, False), False),
            "five-cell exact rank packet changed")
    require(cell_character_rank(representative_cells()) == 5,
            "five-cell weights ceased to be torus-normalizable")

    bridge = sp.zeros(len(LABELS), 1)
    bridge[LABELS.index((0, T))] = 1
    bridge[LABELS.index((1, A))] = -1
    require(representative["phi"] * bridge == sp.zeros(len(WORDS), 1),
            "displayed tilted bridge left the kernel")

    activations = audit_one_cell_activation()
    histogram = Counter(summary for _, summary, _ in activations)
    expected_histogram = Counter({
        (12, 3, 23, 2, (True, True, False), False): 1,
        (13, 2, 17, 2, (True, True, False), False): 2,
        (13, 2, 22, 2, (True, True, False), False): 2,
        (14, 1, 16, 2, (True, True, False), False): 4,
    })
    require(histogram == expected_histogram,
            f"one-cell exact rank histogram changed: {histogram}")
    full_block = audit_full_04_block()

    ledger = {
        "direct_candidates": 9,
        "direct_survivors": [
            {
                "a_edge": list(case["a_edge"]),
                "c_edge": list(case["c_edge"]),
                "dead_holes": list(case["dead_holes"]),
                "summary": list(case["summary"][:4]),
            }
            for case in direct
        ],
        "representative_summary": list(representative["summary"][:4]),
        "one_cell_candidates": 85,
        "one_cell_survivors": 9,
        "activation_histogram": {
            str(key[:4]): value for key, value in sorted(
                histogram.items(), key=lambda item: str(item[0]))
        },
        "full_04_block": full_block,
        "verdict": (
            "the first mixed transgression has one direct bright-completion "
            "orbit; its coefficient-complete 04 endpoint block still has "
            "only the tilted kernel and excludes the missing pure class"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"mixed bright-completion ledger changed: {digest}")

    print("shared reciprocal two-bad mixed bright completion: PASS")
    print("direct bright completions: 2/9, one orbit, each with one dead K_x")
    print("one-cell cofactor activations: 9/85, exactly 04:rs")
    print("all 9 activations: augmented pure intersection = <X_a,X_c>")
    print("full symbolic 04 block: rank 14, kernel <e_t@0-e_a@1>")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
