#!/usr/bin/env python3
"""Independent projective closure for all one-cell invisible deformations.

Starting from the literal nine-cell eight-site quadratic q and its displayed
three-cell polarized preimage z, this checker independently enumerates every
endpoint-colour cell e for which z*(q+t*e)^[3] is unchanged.  It then excludes
the pair-cap equation for every one of those cells and every t != 0.

Only the Python standard library is used; no primary exploration or verifier
module is imported or read.  Coefficients are pairs (constant, coefficient of
t), and every Gram inference is replayed as a literal zero path or odd cycle.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations, permutations, product


SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)

# A cell is (smaller site, larger site, colour at smaller site, colour at
# larger site).  Writing these lists literally keeps endpoint asymmetry visible.
BASE_Q = (
    (2, 3, 0, 0),
    (4, 5, 0, 0),
    (6, 7, 0, 0),
    (0, 1, 1, 1),
    (3, 6, 1, 1),
    (5, 7, 1, 1),
    (0, 2, 2, 2),
    (1, 4, 2, 2),
    (5, 6, 2, 2),
)
DISPLAYED_Z = (
    (0, 1, 0, 0),
    (2, 4, 1, 1),
    (3, 7, 2, 2),
)

PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)
DELTA_WORDS = frozenset(PURE_WORDS)
ZERO = (0, 0)
ONE = (1, 0)
T = (0, 1)

EXPECTED_INVISIBLE_EDGES = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)
EXPECTED_CHANGED_CELLS = (
    (0, 3, 0, 0), (0, 3, 0, 1), (0, 3, 2, 2),
    (0, 4, 0, 0), (0, 4, 0, 2), (0, 4, 1, 1),
    (0, 5, 0, 0), (0, 5, 0, 1), (0, 5, 0, 2),
    (0, 6, 0, 0), (0, 6, 0, 1), (0, 6, 0, 2),
    (0, 7, 0, 0), (0, 7, 0, 1), (0, 7, 0, 2),
    (0, 7, 1, 2), (0, 7, 2, 2),
    (1, 2, 0, 0), (1, 2, 0, 2), (1, 2, 1, 1), (1, 2, 2, 1),
    (1, 3, 0, 0), (1, 3, 0, 1), (1, 3, 2, 2),
    (1, 5, 0, 0),
    (1, 7, 0, 0), (1, 7, 0, 2), (1, 7, 1, 2), (1, 7, 2, 2),
    (2, 5, 1, 0), (2, 5, 1, 1),
    (3, 4, 1, 1), (3, 4, 2, 2),
)
EXPECTED_DIAGONAL_NEW_PURE_EDGES = {
    (0, 3, 0, 0): (((1, 0), (2, 0)),),
    (0, 3, 2, 2): (((2, 2), (7, 2)),),
    (0, 4, 0, 0): (((1, 0), (5, 0)),),
    (0, 4, 1, 1): (((1, 1), (2, 1)),),
    (0, 5, 0, 0): (((1, 0), (4, 0)),),
    (0, 6, 0, 0): (((1, 0), (7, 0)),),
    (0, 7, 0, 0): (((1, 0), (6, 0)),),
    (0, 7, 2, 2): (((2, 2), (3, 2)),),
    (1, 2, 0, 0): (((0, 0), (3, 0)),),
    (1, 2, 1, 1): (((0, 1), (4, 1)),),
    (1, 3, 0, 0): (((0, 0), (2, 0)),),
    (1, 3, 2, 2): (((4, 2), (7, 2)),),
    (1, 5, 0, 0): (((0, 0), (4, 0)),),
    (1, 7, 0, 0): (((0, 0), (6, 0)),),
    (1, 7, 2, 2): (((3, 2), (4, 2)),),
    (2, 5, 1, 1): (((4, 1), (7, 1)),),
    (3, 4, 1, 1): (((2, 1), (6, 1)),),
    (3, 4, 2, 2): (((1, 2), (7, 2)),),
}
EXPECTED_CLASSIFICATION_SHA256 = (
    "05561ea470967c3dbff78bb88b4c7038c2102d356f26cb7f53356b14ad6157b7"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "e1bb9beff9587f2e437f5af2092b6efe64d5d89607051400570a2aed70cac80e"
)

Mode = tuple[int, int]
GramEdge = tuple[Mode, Mode]
Polynomial = tuple[int, int]


@dataclass(frozen=True)
class WeightedCell:
    cell: tuple[int, int, int, int]
    weight: Polynomial


@dataclass(frozen=True)
class ClosureCertificate:
    kind: str
    required_pair: GramEdge
    zero_path: tuple[Mode, ...] = ()
    odd_cycle: tuple[Mode, ...] = ()
    paths_from_cycle: tuple[tuple[Mode, ...], tuple[Mode, ...]] = ((), ())


def add_poly(left: Polynomial, right: Polynomial) -> Polynomial:
    return left[0] + right[0], left[1] + right[1]


def normalized_gram_edge(left: Mode, right: Mode) -> GramEdge:
    assert left != right
    return tuple(sorted((left, right)))


def cell_sites(cell):
    return cell[0], cell[1]


def transform_cell(cell, site_permutation, colour_permutation):
    left, right, left_colour, right_colour = cell
    mapped = (
        (site_permutation[left], colour_permutation[left_colour]),
        (site_permutation[right], colour_permutation[right_colour]),
    )
    mapped = tuple(sorted(mapped))
    return mapped[0][0], mapped[1][0], mapped[0][1], mapped[1][1]


def cells_are_disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell_sites(cell))
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        assert word[left] == word[right] == -1
        word[left] = left_colour
        word[right] = right_colour
    return word


def q_t_cells(extra):
    assert extra not in BASE_Q
    return tuple(WeightedCell(cell, ONE) for cell in BASE_Q) + (
        WeightedCell(extra, T),
    )


def f_and_q_support(extra):
    """Return ps*q_t^[3] forms and q_t^[4] over Z[t]."""
    weighted = q_t_cells(extra)
    f_forms = defaultdict(lambda: defaultdict(lambda: ZERO))
    for chosen in combinations(weighted, 3):
        cells = tuple(item.cell for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        base = partial_word(cells)
        missing = tuple(site for site, value in enumerate(base) if value == -1)
        assert len(missing) == 2
        coefficient = T if any(item.weight == T for item in chosen) else ONE
        for left_colour, right_colour in product(COLOURS, repeat=2):
            word = list(base)
            word[missing[0]] = left_colour
            word[missing[1]] = right_colour
            edge = normalized_gram_edge(
                (missing[0], left_colour), (missing[1], right_colour)
            )
            old = f_forms[tuple(word)][edge]
            f_forms[tuple(word)][edge] = add_poly(old, coefficient)

    q_four = defaultdict(lambda: ZERO)
    for chosen in combinations(weighted, 4):
        cells = tuple(item.cell for item in chosen)
        if not cells_are_disjoint(cells):
            continue
        word = tuple(partial_word(cells))
        assert -1 not in word
        coefficient = T if any(item.weight == T for item in chosen) else ONE
        q_four[word] = add_poly(q_four[word], coefficient)
    return {
        word: dict(form) for word, form in f_forms.items()
    }, dict(q_four)


def polarized_derivative(extra):
    """Compute z*extra*q^[2], the coefficient of t in z*(q+t e)^[3]."""
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for first, second in combinations(BASE_Q, 2):
            chosen = (z_cell, extra, first, second)
            if not cells_are_disjoint(chosen):
                continue
            word = tuple(partial_word(chosen))
            assert -1 not in word
            result[word] += 1
    return result


def base_polarized_expansion():
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for triple in combinations(BASE_Q, 3):
            chosen = (z_cell,) + triple
            if not cells_are_disjoint(chosen):
                continue
            word = tuple(partial_word(chosen))
            result[word] += 1
    return result


# The old seven-coordinate certificate, entered only as a comparison target;
# every coefficient and absence assertion is freshly reconstructed below.
A, B = (0, 0), (1, 0)
C, D = (2, 1), (4, 1)
E, F = (3, 2), (7, 2)
OLD_REQUIRED = (
    normalized_gram_edge(A, B),
    normalized_gram_edge(C, D),
    normalized_gram_edge(E, F),
)
OLD_ZEROS = (
    normalized_gram_edge(A, F),
    normalized_gram_edge(B, F),
    normalized_gram_edge(A, C),
    normalized_gram_edge(C, F),
)
OLD_SEVEN_WORDS = (
    PURE_WORDS[0],
    PURE_WORDS[1],
    PURE_WORDS[2],
    (0, 2, 0, 0, 2, 2, 2, 2),
    (2, 0, 2, 1, 0, 0, 1, 2),
    (0, 2, 1, 1, 2, 1, 1, 1),
    (1, 1, 1, 1, 0, 0, 1, 2),
)
OLD_SEVEN_EDGES = OLD_REQUIRED + OLD_ZEROS


def preserves_old_seven_coordinates(f_forms, q_four):
    for word, expected_edge in zip(OLD_SEVEN_WORDS, OLD_SEVEN_EDGES):
        if f_forms.get(word, {}) != {expected_edge: ONE}:
            return False
        if q_four.get(word, ZERO) != ZERO:
            return False
    return True


def singleton_zero_edges(f_forms, q_four):
    """Use only mixed singleton equations with Q_t identically absent."""
    result = set()
    ledgers = {}
    for word, form in f_forms.items():
        if word in DELTA_WORDS or q_four.get(word, ZERO) != ZERO or len(form) != 1:
            continue
        edge, coefficient = next(iter(form.items()))
        if coefficient not in (ONE, T):
            continue
        result.add(edge)
        ledgers.setdefault(edge, []).append((word, coefficient))
    assert all(entries for entries in ledgers.values())
    return frozenset(result), ledgers


def singleton_pure_edge(f_forms, q_four, colour):
    word = PURE_WORDS[colour]
    assert q_four.get(word, ZERO) == ZERO
    form = f_forms[word]
    if len(form) != 1:
        return None
    edge, coefficient = next(iter(form.items()))
    assert coefficient in (ONE, T)
    return edge


def graph_on_nonzero_modes(required, zero_edges):
    modes = frozenset(mode for edge in required for mode in edge)
    restricted = frozenset(
        edge for edge in zero_edges if edge[0] in modes and edge[1] in modes
    )
    graph = {mode: set() for mode in modes}
    for left, right in restricted:
        graph[left].add(right)
        graph[right].add(left)
    return modes, restricted, {
        mode: tuple(sorted(neighbours)) for mode, neighbours in graph.items()
    }


def path_between(graph, start, finish):
    queue = deque([start])
    parent = {start: None}
    while queue:
        vertex = queue.popleft()
        if vertex == finish:
            break
        for neighbour in graph[vertex]:
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    if finish not in parent:
        return ()
    path = []
    vertex = finish
    while vertex is not None:
        path.append(vertex)
        vertex = parent[vertex]
    return tuple(reversed(path))


def canonical_cycle(cycle_without_repeat):
    cycle = tuple(cycle_without_repeat)
    images = []
    for oriented in (cycle, tuple(reversed(cycle))):
        for shift in range(len(cycle)):
            images.append(oriented[shift:] + oriented[:shift])
    best = min(images)
    return best + (best[0],)


def shortest_odd_cycle(graph, component):
    vertices = tuple(sorted(component))
    for size in range(3, len(vertices) + 1, 2):
        cycles = set()
        for chosen in combinations(vertices, size):
            for ordering in permutations(chosen):
                if all(
                    ordering[(index + 1) % size] in graph[ordering[index]]
                    for index in range(size)
                ):
                    cycles.add(canonical_cycle(ordering))
        if cycles:
            return min(cycles)
    return ()


def projective_certificate(required, zero_edges):
    """Use parity of L -> L^perp, never a union--find inference."""
    modes, restricted, graph = graph_on_nonzero_modes(required, zero_edges)
    component_id = {}
    parity = {}
    components = []
    bipartite = []

    for root in sorted(modes):
        if root in component_id:
            continue
        cid = len(components)
        component_id[root] = cid
        parity[root] = 0
        queue = deque([root])
        vertices = []
        is_bipartite = True
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbour in graph[vertex]:
                if neighbour not in component_id:
                    component_id[neighbour] = cid
                    parity[neighbour] = parity[vertex] ^ 1
                    queue.append(neighbour)
                else:
                    assert component_id[neighbour] == cid
                    if parity[neighbour] == parity[vertex]:
                        is_bipartite = False
        components.append(tuple(sorted(vertices)))
        bipartite.append(is_bipartite)

    for pair in required:
        left, right = pair
        if component_id[left] != component_id[right]:
            continue
        cid = component_id[left]
        if bipartite[cid]:
            if parity[left] == parity[right]:
                continue
            path = path_between(graph, left, right)
            assert path and (len(path) - 1) % 2 == 1
            return ClosureCertificate("odd_zero_path", pair, zero_path=path), restricted

        cycle = shortest_odd_cycle(graph, components[cid])
        assert cycle
        root = cycle[0]
        return ClosureCertificate(
            "isotropic_component",
            pair,
            odd_cycle=cycle,
            paths_from_cycle=(
                path_between(graph, root, left),
                path_between(graph, root, right),
            ),
        ), restricted
    return None, restricted


def validate_walk(graph, walk):
    assert walk
    for left, right in zip(walk, walk[1:]):
        assert right in graph[left]


def validate_certificate(certificate, required, restricted_zero_edges):
    """Replay the literal path/cycle facts supporting the contradiction."""
    assert certificate.required_pair in required
    modes, reconstructed, graph = graph_on_nonzero_modes(
        required, restricted_zero_edges
    )
    assert reconstructed == restricted_zero_edges
    assert modes == frozenset(graph)
    left, right = certificate.required_pair
    if certificate.kind == "odd_zero_path":
        path = certificate.zero_path
        assert path[0] == left and path[-1] == right
        validate_walk(graph, path)
        assert (len(path) - 1) % 2 == 1
        return

    assert certificate.kind == "isotropic_component"
    cycle = certificate.odd_cycle
    assert cycle[0] == cycle[-1]
    assert len(set(cycle[:-1])) == len(cycle) - 1
    validate_walk(graph, cycle)
    assert (len(cycle) - 1) % 2 == 1
    left_path, right_path = certificate.paths_from_cycle
    assert left_path[0] == cycle[0] == right_path[0]
    assert left_path[-1] == left and right_path[-1] == right
    validate_walk(graph, left_path)
    validate_walk(graph, right_path)


def main():
    assert len(ALL_CELLS) == 28 * 9 == 252
    assert len(set(BASE_Q)) == 9 and len(set(DISPLAYED_Z)) == 3
    assert base_polarized_expansion() == Counter({word: 1 for word in PURE_WORDS})

    # There is no nontrivial literal site/colour orbit reduction for this
    # asymmetric seed: its stabilizer inside S_8 x S_3 is the identity.
    base_support = frozenset(BASE_Q)
    stabilizer_size = 0
    for site_permutation in permutations(SITES):
        for colour_permutation in permutations(COLOURS):
            image = frozenset(
                transform_cell(cell, site_permutation, colour_permutation)
                for cell in BASE_Q
            )
            stabilizer_size += int(image == base_support)
    assert stabilizer_size == 1

    invisible = tuple(cell for cell in ALL_CELLS if not polarized_derivative(cell))
    assert len(invisible) == 99
    assert all(cell not in BASE_Q for cell in invisible)
    invisible_edges = tuple(sorted({cell_sites(cell) for cell in invisible}))
    assert invisible_edges == EXPECTED_INVISIBLE_EDGES
    assert all(sum(cell_sites(cell) == edge for cell in invisible) == 9 for edge in invisible_edges)

    preserved = []
    changed = []
    off_diagonal_closed = []
    diagonal_closed = []
    classification_digest = hashlib.sha256()
    certificate_digest = hashlib.sha256()
    certificate_kinds = Counter()
    cycle_sizes = Counter()

    for extra in invisible:
        f_forms, q_four = f_and_q_support(extra)
        if preserves_old_seven_coordinates(f_forms, q_four):
            category = "old-seven"
            preserved.append(extra)
            # Replay the original graph contradiction rather than merely
            # trusting the seven labels.
            certificate, restricted = projective_certificate(
                OLD_REQUIRED, frozenset(OLD_ZEROS)
            )
            assert certificate is not None
            validate_certificate(certificate, OLD_REQUIRED, restricted)
        else:
            changed.append(extra)
            zero_edges, zero_ledger = singleton_zero_edges(f_forms, q_four)
            assert all(
                coefficient in (ONE, T)
                for entries in zero_ledger.values()
                for _word, coefficient in entries
            )

            if extra[2] != extra[3]:
                category = "off-diagonal-projective"
                required = tuple(
                    singleton_pure_edge(f_forms, q_four, colour)
                    for colour in COLOURS
                )
                assert all(required)
                assert required == OLD_REQUIRED
                certificate, restricted = projective_certificate(required, zero_edges)
                assert certificate is not None
                validate_certificate(certificate, required, restricted)
                off_diagonal_closed.append(extra)
                certificate_kinds[certificate.kind] += 1
                if certificate.odd_cycle:
                    cycle_sizes[len(certificate.odd_cycle) - 1] += 1
                record = (
                    extra, "single", required, tuple(sorted(restricted)), certificate
                )
                certificate_digest.update(repr(record).encode())
                certificate_digest.update(b"\n")
            else:
                category = "diagonal-two-branch"
                affected_colour = extra[2]
                unaffected_required = []
                for colour in COLOURS:
                    if colour == affected_colour:
                        continue
                    edge = singleton_pure_edge(f_forms, q_four, colour)
                    assert edge == OLD_REQUIRED[colour]
                    unaffected_required.append(edge)

                affected_word = PURE_WORDS[affected_colour]
                assert q_four.get(affected_word, ZERO) == ZERO
                affected_form = f_forms[affected_word]
                assert len(affected_form) == 2
                coefficient_multiset = Counter(affected_form.values())
                assert coefficient_multiset == Counter({ONE: 1, T: 1})
                assert OLD_REQUIRED[affected_colour] in affected_form
                assert affected_form[OLD_REQUIRED[affected_colour]] == ONE
                new_edges = tuple(
                    edge for edge in affected_form
                    if edge != OLD_REQUIRED[affected_colour]
                )
                assert new_edges == EXPECTED_DIAGONAL_NEW_PURE_EDGES[extra]
                assert affected_form[new_edges[0]] == T

                # R_old + t R_new = 1/4.  Since t != 0, at least one
                # displayed Gram term is nonzero; close both possibilities.
                for branch, affected_edge in enumerate(sorted(affected_form)):
                    required = tuple(unaffected_required + [affected_edge])
                    certificate, restricted = projective_certificate(required, zero_edges)
                    assert certificate is not None
                    validate_certificate(certificate, required, restricted)
                    certificate_kinds[certificate.kind] += 1
                    if certificate.odd_cycle:
                        cycle_sizes[len(certificate.odd_cycle) - 1] += 1
                    record = (
                        extra, branch, affected_edge, required,
                        tuple(sorted(restricted)), certificate,
                    )
                    certificate_digest.update(repr(record).encode())
                    certificate_digest.update(b"\n")
                diagonal_closed.append(extra)

        classification_digest.update(repr((extra, category)).encode())
        classification_digest.update(b"\n")

    assert len(preserved) == 66
    assert len(changed) == 33
    assert tuple(changed) == EXPECTED_CHANGED_CELLS
    assert len(off_diagonal_closed) == 15
    assert len(diagonal_closed) == 18
    assert len(preserved) + len(off_diagonal_closed) + len(diagonal_closed) == 99
    assert all(cell[2] != cell[3] for cell in off_diagonal_closed)
    assert all(cell[2] == cell[3] for cell in diagonal_closed)
    assert certificate_kinds == Counter({"isotropic_component": 51})

    assert classification_digest.hexdigest() == EXPECTED_CLASSIFICATION_SHA256
    assert certificate_digest.hexdigest() == EXPECTED_CERTIFICATE_SHA256

    print("independent one-cell invisible-direction closure: PASS")
    print("literal S_8 x S_3 stabilizer of the nine-cell seed is trivial: PASS")
    print("252 endpoint-colour cells scanned; exactly 99 invisible: PASS")
    print("11 invisible physical edges, each with all 9 endpoint colours: PASS")
    print("66 additions retain the old seven coordinates literally: PASS")
    print("15 off-diagonal changed cases close projectively: PASS")
    print("18 diagonal cases and all 36 nonzero branches close projectively: PASS")
    print(f"hard-case certificate kinds: {dict(sorted(certificate_kinds.items()))}")
    print(f"odd-cycle sizes: {dict(sorted(cycle_sizes.items()))}")
    print(f"classification SHA-256: {classification_digest.hexdigest()}")
    print(f"certificate SHA-256: {certificate_digest.hexdigest()}")
    print("all 99 families exclude the pair-cap equation for every t != 0: PASS")


if __name__ == "__main__":
    main()
