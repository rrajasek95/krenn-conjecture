#!/usr/bin/env python3
"""Clean-room support theorem for one full invisible 3x3 physical block.

For each of the eleven physical pairs invisible to the displayed polarized
preimage, add an arbitrary endpoint-colour block to the literal nine-cell
quadratic.  Every support mask is checked using only:

* pure-coordinate branching on individual nonzero summands;
* mixed coordinates with one literal Gram contributor and no q^[4] support;
* projective orthogonality certificates replayed as paths or odd cycles.

No primary exploration or verifier module is imported or read.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations, permutations, product
import shutil
import subprocess
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))
BASE_ATOM = -1

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
INVISIBLE_PAIRS = (
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 2), (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
)
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)
PURE_WORD_SET = frozenset(PURE_WORDS)
DISCOVERY_MINIMAL_OPEN_17 = (33, 38, 258, 261)
MINIMAL_OPEN_17 = (261, 291)

EXPECTED_CLASSIFICATION_SHA256 = (
    "661e57a22c1eb5f308e09d5cd2fc8a9360fe16dbe01aee0fb65d30ed0495359a"
)
EXPECTED_BRANCH_LEDGER_SHA256 = (
    "258a5e409eeced43ea4e777c46d72ab0e761de29df9f1bafeeab27ef13fcf757"
)
EXPECTED_PAIR17_EQUATION_SHA256 = (
    "1b4777acae6a7db26a51cc613cce1be34a8d16af8e94678d40bf8fed59c3cb2e"
)

Mode = tuple[int, int]
GramEdge = tuple[Mode, Mode]


@dataclass(frozen=True)
class Contribution:
    edge: GramEdge
    atom: int


@dataclass(frozen=True)
class ClosureCertificate:
    kind: str
    required_pair: GramEdge
    zero_path: tuple[Mode, ...] = ()
    odd_cycle: tuple[Mode, ...] = ()
    paths_from_cycle: tuple[tuple[Mode, ...], tuple[Mode, ...]] = ((), ())


def normalized_edge(left: Mode, right: Mode) -> GramEdge:
    assert left != right
    return tuple(sorted((left, right)))


def block_cells(pair):
    return tuple(
        (pair[0], pair[1], left_colour, right_colour)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )


def disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell[:2])
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        assert word[left] == word[right] == -1
        word[left] = left_colour
        word[right] = right_colour
    return word


def append_f_contributions(target, cells, atom):
    base = partial_word(cells)
    missing = tuple(site for site, colour in enumerate(base) if colour == -1)
    assert len(missing) == 2
    for left_colour, right_colour in product(COLOURS, repeat=2):
        word = list(base)
        word[missing[0]] = left_colour
        word[missing[1]] = right_colour
        edge = normalized_edge(
            (missing[0], left_colour), (missing[1], right_colour)
        )
        target[tuple(word)].append(Contribution(edge, atom))


def base_maps():
    f_map = defaultdict(list)
    for chosen in combinations(BASE_Q, 3):
        if disjoint(chosen):
            append_f_contributions(f_map, chosen, BASE_ATOM)

    q_support = set()
    for chosen in combinations(BASE_Q, 4):
        if not disjoint(chosen):
            continue
        word = tuple(partial_word(chosen))
        assert -1 not in word
        q_support.add(word)
    return {word: tuple(terms) for word, terms in f_map.items()}, frozenset(q_support)


BASE_F_MAP, BASE_Q_SUPPORT = base_maps()


def cell_variation(cell, atom):
    f_map = defaultdict(list)
    for chosen_base in combinations(BASE_Q, 2):
        chosen = (cell,) + chosen_base
        if disjoint(chosen):
            append_f_contributions(f_map, chosen, atom)

    q_support = set()
    for chosen_base in combinations(BASE_Q, 3):
        chosen = (cell,) + chosen_base
        if not disjoint(chosen):
            continue
        word = tuple(partial_word(chosen))
        assert -1 not in word
        q_support.add(word)
    return {word: tuple(terms) for word, terms in f_map.items()}, frozenset(q_support)


def polarized_derivative(cell):
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for chosen_base in combinations(BASE_Q, 2):
            chosen = (z_cell, cell) + chosen_base
            if not disjoint(chosen):
                continue
            word = tuple(partial_word(chosen))
            assert -1 not in word
            result[word] += 1
    return result


def base_polarized_expansion():
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for chosen_base in combinations(BASE_Q, 3):
            chosen = (z_cell,) + chosen_base
            if not disjoint(chosen):
                continue
            word = tuple(partial_word(chosen))
            assert -1 not in word
            result[word] += 1
    return result


def merge_support_map(pair, mask, variations):
    f_map = defaultdict(list)
    for word, contributions in BASE_F_MAP.items():
        f_map[word].extend(contributions)
    q_support = set(BASE_Q_SUPPORT)

    cells = block_cells(pair)
    for atom, cell in enumerate(cells):
        if not (mask & (1 << atom)):
            continue
        varied_f, varied_q = variations[cell]
        for word, contributions in varied_f.items():
            f_map[word].extend(contributions)
        q_support.update(varied_q)
    return {word: tuple(terms) for word, terms in f_map.items()}, frozenset(q_support)


def singleton_zero_data(f_map, q_support):
    edges = set()
    ledger = {}
    for word, contributions in f_map.items():
        if word in PURE_WORD_SET or word in q_support or len(contributions) != 1:
            continue
        contribution = contributions[0]
        edges.add(contribution.edge)
        ledger[word] = contribution
    return frozenset(edges), ledger


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
            return ClosureCertificate(
                "odd_zero_path", pair, zero_path=path
            ), restricted

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
    assert certificate.required_pair in required
    modes, reconstructed, graph = graph_on_nonzero_modes(
        required, restricted_zero_edges
    )
    assert modes == frozenset(graph)
    assert reconstructed == restricted_zero_edges
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


def minimal_masks(masks):
    masks = tuple(sorted(masks))
    return tuple(
        mask for mask in masks
        if not any(other != mask and (other & mask) == other for other in masks)
    )


def mode_variable(prefix, mode):
    return f"{prefix}{mode[0]}{mode[1]}"


def atom_variable(atom):
    if atom == BASE_ATOM:
        return "1"
    return f"h{atom // 3}{atom % 3}"


def beta_expression(edge):
    left, right = edge
    return (
        f"{mode_variable('p', left)}*{mode_variable('s', right)}"
        f"+{mode_variable('s', left)}*{mode_variable('p', right)}"
    )


def full_pair17_coordinate_equations():
    """Build all top-coordinate equations independently over QQ.

    The variable block order is deliberately block weights, the scalar a,
    all p-coordinates, then all s-coordinates.  This differs from the
    interleaved-vector order used by the geometric certificate code.
    """
    pair = (1, 7)
    cells = block_cells(pair)
    variations = {
        cell: cell_variation(cell, atom)
        for atom, cell in enumerate(cells)
    }
    f_map, _q_support = merge_support_map(pair, 511, variations)

    q_atoms = defaultdict(list)
    for chosen in combinations(BASE_Q, 4):
        if disjoint(chosen):
            word = tuple(partial_word(chosen))
            q_atoms[word].append(BASE_ATOM)
    for atom, cell in enumerate(cells):
        for chosen_base in combinations(BASE_Q, 3):
            chosen = (cell,) + chosen_base
            if not disjoint(chosen):
                continue
            word = tuple(partial_word(chosen))
            q_atoms[word].append(atom)

    words = tuple(sorted(set(f_map) | set(q_atoms) | PURE_WORD_SET))
    equations = []
    records = []
    for word in words:
        summands = []
        for atom in q_atoms.get(word, ()):
            weight = atom_variable(atom)
            summands.append("aa" if weight == "1" else f"aa*{weight}")
        for contribution in f_map.get(word, ()):
            beta = beta_expression(contribution.edge)
            weight = atom_variable(contribution.atom)
            summands.append(f"({beta})" if weight == "1" else f"{weight}*({beta})")
        target = int(word in PURE_WORD_SET)
        assert summands or target
        expression = "4*(" + "+".join(summands) + ")"
        if target:
            expression += "-1"
        equations.append(expression)
        records.append((
            word,
            tuple(q_atoms.get(word, ())),
            tuple(f_map.get(word, ())),
            target,
        ))
    assert len(equations) == len(records) == 545
    digest = hashlib.sha256()
    for record in records:
        digest.update(repr(record).encode())
        digest.update(b"\n")
    return tuple(equations), digest.hexdigest()


def pair17_unsaturated_unit_ideal():
    """Run a second exact route on the 80 projective-frontier masks.

    The ideal has the nine block coefficients as ordinary affine variables,
    with no saturation or nonvanishing assumptions.  A unit ideal therefore
    excludes every specialization, including every support mask.
    """
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required for the pair-17 exact ideal audit")

    equations, digest = full_pair17_coordinate_equations()
    assert digest == EXPECTED_PAIR17_EQUATION_SHA256

    h_variables = tuple(f"h{left}{right}" for left in COLOURS for right in COLOURS)
    p_variables = tuple(
        mode_variable("p", (site, colour))
        for site in SITES for colour in COLOURS
    )
    s_variables = tuple(
        mode_variable("s", (site, colour))
        for site in SITES for colour in COLOURS
    )
    variables = h_variables + ("aa",) + p_variables + s_variables
    assert len(variables) == 58 and len(set(variables)) == 58

    program = (
        "ring r=0,(" + ",".join(variables) + "),dp;\n"
        "option(redSB);\n"
        "ideal I=" + ",\n".join(equations) + ";\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE");\n'
        "print(size(G));\n"
        'print("BASIS_FIRST");\n'
        "print(G[1]);\n"
    )
    started = time.monotonic()
    result = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=180,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    size_index = lines.index("BASIS_SIZE")
    first_index = lines.index("BASIS_FIRST")
    assert lines[size_index + 1] == "1", result.stdout
    assert lines[first_index + 1] == "1", result.stdout
    return digest, elapsed


def main():
    assert len(BASE_F_MAP) == 165
    assert sum(map(len, BASE_F_MAP.values())) == 171
    assert BASE_Q_SUPPORT == {
        (1, 1, 0, 0, 0, 0, 0, 0),
        (2, 2, 2, 1, 2, 1, 1, 1),
    }
    assert base_polarized_expansion() == Counter({word: 1 for word in PURE_WORDS})

    classification_digest = hashlib.sha256()
    branch_digest = hashlib.sha256()
    pair_counts = {}
    pair_branch_counts = {}
    certificate_kinds = Counter()
    cycle_sizes = Counter()
    total_closed_branches = 0
    total_open_branches = 0

    for pair in INVISIBLE_PAIRS:
        cells = block_cells(pair)
        assert len(cells) == len(set(cells)) == 9
        assert all(not polarized_derivative(cell) for cell in cells)
        variations = {
            cell: cell_variation(cell, atom)
            for atom, cell in enumerate(cells)
        }

        closed_masks = []
        open_masks = []
        branches_for_pair = 0
        open_branches_for_pair = 0
        for mask in range(1 << 9):
            f_map, q_support = merge_support_map(pair, mask, variations)
            zero_edges, zero_ledger = singleton_zero_data(f_map, q_support)
            assert all(
                contribution.atom == BASE_ATOM
                or mask & (1 << contribution.atom)
                for contribution in zero_ledger.values()
            )

            pure_options = []
            for word in PURE_WORDS:
                assert word not in q_support
                contributions = f_map.get(word, ())
                assert contributions
                assert all(
                    contribution.atom == BASE_ATOM
                    or mask & (1 << contribution.atom)
                    for contribution in contributions
                )
                pure_options.append(tuple(contribution.edge for contribution in contributions))

            mask_closed = True
            branch_count = 0
            open_branch_count = 0
            for branch in product(*pure_options):
                branch_count += 1
                certificate, restricted = projective_certificate(branch, zero_edges)
                if certificate is None:
                    mask_closed = False
                    open_branch_count += 1
                    branch_record = (
                        pair, mask, branch, tuple(sorted(restricted)), "OPEN"
                    )
                else:
                    validate_certificate(certificate, branch, restricted)
                    certificate_kinds[certificate.kind] += 1
                    if certificate.odd_cycle:
                        cycle_sizes[len(certificate.odd_cycle) - 1] += 1
                    branch_record = (
                        pair, mask, branch, tuple(sorted(restricted)), certificate
                    )
                branch_digest.update(repr(branch_record).encode())
                branch_digest.update(b"\n")

            assert branch_count > 0
            branches_for_pair += branch_count
            open_branches_for_pair += open_branch_count
            if mask_closed:
                assert open_branch_count == 0
                closed_masks.append(mask)
                total_closed_branches += branch_count
            else:
                assert open_branch_count > 0
                open_masks.append(mask)
                total_closed_branches += branch_count - open_branch_count
                total_open_branches += open_branch_count

            classification_record = (
                pair, mask, int(mask_closed), branch_count, open_branch_count
            )
            classification_digest.update(repr(classification_record).encode())
            classification_digest.update(b"\n")

        pair_counts[pair] = (len(closed_masks), len(open_masks))
        pair_branch_counts[pair] = (branches_for_pair, open_branches_for_pair)
        if pair != (1, 7):
            assert len(closed_masks) == 512 and not open_masks
        else:
            # The discovery union--find reported 256/256 with four minimal
            # open masks.  Exact projective parity is strictly stronger:
            # masks 33, 38, and 258 close, leaving these two minimal masks.
            assert len(closed_masks) == 432 and len(open_masks) == 80
            assert minimal_masks(open_masks) == MINIMAL_OPEN_17
            assert all(
                mask not in open_masks
                for mask in DISCOVERY_MINIMAL_OPEN_17[:3]
            )
            assert DISCOVERY_MINIMAL_OPEN_17[3] in open_masks
            predicted_open = tuple(
                mask for mask in range(512)
                if any((mask & core) == core for core in MINIMAL_OPEN_17)
            )
            assert tuple(open_masks) == predicted_open

    assert sum(closed for closed, _open in pair_counts.values()) == 5_552
    assert sum(open_count for _closed, open_count in pair_counts.values()) == 80
    assert classification_digest.hexdigest() == EXPECTED_CLASSIFICATION_SHA256
    assert branch_digest.hexdigest() == EXPECTED_BRANCH_LEDGER_SHA256
    pair17_equation_digest, pair17_ideal_seconds = pair17_unsaturated_unit_ideal()

    print("independent invisible-block projective frontier: PASS")
    for pair in INVISIBLE_PAIRS:
        print(
            f"pair {pair}: closed/open masks {pair_counts[pair]}, "
            f"branches/open branches {pair_branch_counts[pair]}"
        )
    print("10 physical pairs: all 512 supports closed")
    print("pair (1, 7): 432 closed, 80 projective-frontier supports")
    print(f"weaker discovery minima superseded: {DISCOVERY_MINIMAL_OPEN_17}")
    print(f"minimal pair-17 frontier masks: {MINIMAL_OPEN_17}")
    print(f"certificate kinds: {dict(sorted(certificate_kinds.items()))}")
    print(f"odd-cycle sizes: {dict(sorted(cycle_sizes.items()))}")
    print(f"closed/open branches globally: {total_closed_branches}/{total_open_branches}")
    print(f"classification SHA-256: {classification_digest.hexdigest()}")
    print(f"branch-ledger SHA-256: {branch_digest.hexdigest()}")
    print(f"pair-17 equation SHA-256: {pair17_equation_digest}")
    print(
        "pair-17 unsaturated 545-equation ideal is [1]: PASS "
        f"({pair17_ideal_seconds:.3f}s)"
    )
    print("all 11 invisible blocks and all 512 support masks excluded: PASS")
    print("support-only weighted block theorem and exact frontier: PASS")


if __name__ == "__main__":
    main()
